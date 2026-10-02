import json
import asyncio
from typing import List, Dict, Any, Optional, Callable, Awaitable
from backend.app.config import settings
from backend.app.cube.engine import CubeEngine
from backend.app.tools.cube_tools import CubeTools
from backend.app.tools.registry import ToolRegistry
from backend.app.services.groq_client import groq_client
from backend.app.agent.prompts import SYSTEM_PROMPT


class AgentOrchestrator:
    def __init__(self, engine: CubeEngine):
        self.engine = engine
        self.cube_tools = CubeTools(engine)
        self.registry = ToolRegistry(self.cube_tools)
        self.max_turns = settings.MAX_AGENT_TURNS

    async def run(
        self,
        user_prompt: str = "Please analyze and solve the current Rubik's Cube state.",
        event_callback: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    ) -> Dict[str, Any]:
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        initial_state = self.engine.get_state()
        turns = 0
        executed_moves: List[str] = []
        logs: List[Dict[str, Any]] = []

        if event_callback:
            await event_callback({
                "type": "status",
                "status": "INITIALIZING",
                "message": "AI Agent initialized. Preparing to inspect cube.",
            })

        while turns < self.max_turns:
            turns += 1

            response_msg = groq_client.create_chat_completion(
                messages=messages,
                tools=self.registry.get_schemas(),
            )

            messages.append(response_msg)

            tool_calls = response_msg.get("tool_calls")
            if not tool_calls:
                final_text = response_msg.get("content") or "Cube solve workflow completed."
                final_moves = self.cube_tools.solver.prune_to_solved(initial_state, executed_moves)
                if event_callback:
                    await event_callback({
                        "type": "final",
                        "status": "COMPLETED",
                        "message": final_text,
                        "is_solved": self.engine.is_solved(),
                        "moves": final_moves,
                    })
                return {
                    "status": "COMPLETED",
                    "turns": turns,
                    "explanation": final_text,
                    "is_solved": self.engine.is_solved(),
                    "moves": final_moves,
                    "logs": logs,
                }

            for tc in tool_calls:
                call_id = tc["id"]
                fn_name = tc["function"]["name"]
                raw_args = tc["function"].get("arguments", "{}")

                try:
                    args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                except Exception:
                    args = {}

                if event_callback:
                    await event_callback({
                        "type": "tool_call",
                        "tool": fn_name,
                        "args": args,
                        "turn": turns,
                    })

                result = self.registry.execute(fn_name, args)

                logs.append({
                    "turn": turns,
                    "tool": fn_name,
                    "args": args,
                    "result": result,
                })

                if fn_name == "apply_moves" and "applied_moves" in result:
                    new_moves = result["applied_moves"]
                    executed_moves.extend(new_moves)
                    if event_callback:
                        for idx, m in enumerate(new_moves):
                            await event_callback({
                                "type": "move",
                                "move": m,
                                "move_index": idx + 1,
                                "total_moves": len(new_moves),
                                "state": self.engine.get_state(),
                            })
                            await asyncio.sleep(0.05)

                if event_callback:
                    await event_callback({
                        "type": "tool_result",
                        "tool": fn_name,
                        "result": result,
                        "turn": turns,
                    })

                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "name": fn_name,
                    "content": json.dumps(result),
                })

            if self.engine.is_solved() and executed_moves:
                final_moves = self.cube_tools.solver.prune_to_solved(initial_state, executed_moves)
                if event_callback:
                    await event_callback({
                        "type": "final",
                        "status": "COMPLETED",
                        "message": "Cube successfully solved.",
                        "is_solved": True,
                        "moves": final_moves,
                    })
                return {
                    "status": "COMPLETED",
                    "turns": turns,
                    "explanation": "Cube successfully solved.",
                    "is_solved": True,
                    "moves": final_moves,
                    "logs": logs,
                }

        final_moves = self.cube_tools.solver.prune_to_solved(initial_state, executed_moves)
        return {
            "status": "MAX_TURNS_REACHED",
            "turns": turns,
            "explanation": "Max agent turns reached. Current state preserved.",
            "is_solved": self.engine.is_solved(),
            "moves": final_moves,
            "logs": logs,
        }
