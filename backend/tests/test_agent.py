import pytest
import asyncio
from backend.app.cube.engine import CubeEngine
from backend.app.agent.orchestrator import AgentOrchestrator


@pytest.mark.asyncio
async def test_agent_orchestrator_solves_scrambled_cube():
    engine = CubeEngine()
    engine.apply_moves(["R", "U", "R'", "U'"])
    assert not engine.is_solved()

    orchestrator = AgentOrchestrator(engine)
    result = await orchestrator.run()

    assert result["status"] == "COMPLETED"
    assert engine.is_solved()
    assert len(result["moves"]) > 0


@pytest.mark.asyncio
async def test_agent_orchestrator_streaming_events():
    engine = CubeEngine()
    engine.apply_moves(["F", "F'"])
    events = []

    async def callback(evt):
        events.append(evt)

    orchestrator = AgentOrchestrator(engine)
    result = await orchestrator.run(event_callback=callback)

    assert result["status"] == "COMPLETED"
    assert len(events) > 0
    event_types = [e["type"] for e in events]
    assert "status" in event_types
    assert "tool_call" in event_types
