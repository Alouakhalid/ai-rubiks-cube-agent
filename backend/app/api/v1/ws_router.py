import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Any, Optional
from backend.app.services.session_manager import session_manager
from backend.app.agent.orchestrator import AgentOrchestrator

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    engine = session_manager.get_session(session_id)
    solve_task: Optional[asyncio.Task] = None

    async def send_event(data: Dict[str, Any]):
        try:
            await websocket.send_text(json.dumps(data))
        except Exception:
            pass

    try:
        while True:
            raw_text = await websocket.receive_text()
            try:
                payload = json.loads(raw_text)
            except Exception:
                continue

            action = payload.get("action")

            if action == "ping":
                await send_event({"type": "pong"})

            elif action == "start_solve":
                if solve_task and not solve_task.done():
                    solve_task.cancel()

                orchestrator = AgentOrchestrator(engine)
                prompt = payload.get("prompt", "Analyze and solve the cube.")

                solve_task = asyncio.create_task(
                    orchestrator.run(user_prompt=prompt, event_callback=send_event)
                )

            elif action == "stop_solve":
                if solve_task and not solve_task.done():
                    solve_task.cancel()
                    await send_event({
                        "type": "status",
                        "status": "STOPPED",
                        "message": "AI solving aborted by user.",
                        "state": engine.get_state(),
                    })

    except WebSocketDisconnect:
        if solve_task and not solve_task.done():
            solve_task.cancel()
