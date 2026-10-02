import pytest
from backend.app.cube.engine import CubeEngine
from backend.app.tools.cube_tools import CubeTools
from backend.app.tools.registry import ToolRegistry


def test_cube_tools_get_state():
    engine = CubeEngine()
    tools = CubeTools(engine)
    res = tools.get_cube_state()
    assert res["is_solved"]
    assert len(res["facelets"]) == 54


def test_cube_tools_validate_cube():
    engine = CubeEngine()
    tools = CubeTools(engine)
    res = tools.validate_cube()
    assert res["is_valid"]


def test_cube_tools_scramble_and_apply_moves():
    engine = CubeEngine()
    tools = CubeTools(engine)
    scramble_res = tools.scramble_cube(length=5)
    assert len(scramble_res["scramble_sequence"]) == 5
    assert not scramble_res["is_solved"]

    engine.reset()
    apply_res = tools.apply_moves(["R", "R'"])
    assert apply_res["is_solved"]


def test_tool_registry_execution():
    engine = CubeEngine()
    tools = CubeTools(engine)
    registry = ToolRegistry(tools)

    schemas = registry.get_schemas()
    assert len(schemas) >= 9

    state_res = registry.execute("get_cube_state", {})
    assert state_res["is_solved"]

    kb_res = registry.execute("query_knowledge_base", {"query": "CFOP"})
    assert kb_res["results_count"] > 0
