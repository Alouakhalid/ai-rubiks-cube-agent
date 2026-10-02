from fastapi import APIRouter
from typing import Dict, Any
from backend.app.services.session_manager import session_manager
from backend.app.agent.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/solve")
async def solve_cube_sync(session_id: str = "default", prompt: str = "Analyze and solve the cube.") -> Dict[str, Any]:
    engine = session_manager.get_session(session_id)
    orchestrator = AgentOrchestrator(engine)
    result = await orchestrator.run(user_prompt=prompt)
    return result
