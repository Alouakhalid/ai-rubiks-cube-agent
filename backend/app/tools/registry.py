import json
from typing import Dict, Any, List, Callable
from backend.app.tools.cube_tools import CubeTools


class ToolRegistry:
    def __init__(self, cube_tools: CubeTools):
        self.cube_tools = cube_tools
        self.handlers: Dict[str, Callable[..., Any]] = {
            "get_cube_state": self.cube_tools.get_cube_state,
            "get_cube_summary": self.cube_tools.get_cube_summary,
            "get_legal_moves": self.cube_tools.get_legal_moves,
            "validate_cube": self.cube_tools.validate_cube,
            "solve_cube_algorithmic": self.cube_tools.solve_cube_algorithmic,
            "apply_moves": self.cube_tools.apply_moves,
            "check_solved": self.cube_tools.check_solved,
            "reset_cube": self.cube_tools.reset_cube,
            "scramble_cube": self.cube_tools.scramble_cube,
            "query_knowledge_base": self.cube_tools.query_knowledge_base,
        }

    def get_schemas(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_cube_state",
                    "description": "Returns current 54-facelet representation, solved status, and recent move history.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_cube_summary",
                    "description": "Returns high-level summary of face uniformities and scramble history.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_legal_moves",
                    "description": "Returns the list of valid Singmaster moves.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "validate_cube",
                    "description": "Validates physical solvability using group theory parity invariants.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "solve_cube_algorithmic",
                    "description": "Computes optimal solution moves using the deterministic solver.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "max_length": {
                                "type": "integer",
                                "description": "Maximum move count allowed.",
                                "default": 21,
                            }
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "apply_moves",
                    "description": "Applies a sequence of Singmaster moves to the cube engine.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "moves": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of moves, e.g. ['R', 'U', \"R'\", 'F2'].",
                            }
                        },
                        "required": ["moves"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "check_solved",
                    "description": "Checks if all faces are uniformly colored.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "reset_cube",
                    "description": "Resets the cube to standard solved state.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "scramble_cube",
                    "description": "Scrambles the cube with random non-canceling moves.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "length": {
                                "type": "integer",
                                "description": "Number of moves in scramble.",
                                "default": 20,
                            }
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "query_knowledge_base",
                    "description": "Retrieves peer-reviewed literature and speedcubing theory (Kociemba, CFOP, God's Number, WCA).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Keywords or question regarding cube mathematics or methods.",
                            }
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.handlers:
            return {"error": f"Unknown tool: {tool_name}"}

        handler = self.handlers[tool_name]
        try:
            return handler(**arguments)
        except Exception as e:
            return {"error": str(e)}
