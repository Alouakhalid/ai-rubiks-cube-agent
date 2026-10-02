from typing import Dict, Any, List
from backend.app.cube.engine import CubeEngine
from backend.app.cube.validator import CubeValidator
from backend.app.solver.kociemba_solver import KociembaSolver
from backend.app.rag.knowledge_base import knowledge_base
from backend.app.cube.constants import VALID_MOVES


class CubeTools:
    def __init__(self, engine: CubeEngine):
        self.engine = engine
        self.solver = KociembaSolver()
        self.kb = knowledge_base

    def get_cube_state(self) -> Dict[str, Any]:
        return {
            "facelets": self.engine.get_state(),
            "is_solved": self.engine.is_solved(),
            "move_history_length": len(self.engine.move_history),
            "recent_moves": self.engine.move_history[-10:],
        }

    def get_cube_summary(self) -> Dict[str, Any]:
        state = self.engine.get_state()
        solved = self.engine.is_solved()
        face_uniformity: Dict[str, bool] = {}
        for idx, face in enumerate(["U", "R", "F", "D", "L", "B"]):
            chars = state[idx * 9 : (idx + 1) * 9]
            face_uniformity[face] = len(set(chars)) == 1

        return {
            "is_solved": solved,
            "face_uniformity": face_uniformity,
            "total_moves_applied": len(self.engine.move_history),
            "scramble_history": self.engine.scramble_history,
        }

    def get_legal_moves(self) -> List[str]:
        return VALID_MOVES

    def validate_cube(self) -> Dict[str, Any]:
        result = CubeValidator.validate_state(self.engine.get_state())
        return {
            "is_valid": result.is_valid,
            "message": result.message,
            "details": result.details,
        }

    def solve_cube_algorithmic(self, max_length: int = 21) -> Dict[str, Any]:
        val = CubeValidator.validate_state(self.engine.get_state())
        if not val.is_valid:
            return {
                "success": False,
                "error": f"Cannot solve invalid cube: {val.message}",
                "solution": [],
            }

        solution_moves = self.solver.solve(
            self.engine.get_state(),
            hint_history=self.engine.move_history,
        )

        return {
            "success": True,
            "solution": solution_moves,
            "move_count": len(solution_moves),
        }

    def apply_moves(self, moves: List[str]) -> Dict[str, Any]:
        applied: List[str] = []
        for m in moves:
            if m in VALID_MOVES:
                self.engine.apply_move(m)
                applied.append(m)

        return {
            "applied_moves": applied,
            "facelets": self.engine.get_state(),
            "is_solved": self.engine.is_solved(),
        }

    def check_solved(self) -> Dict[str, Any]:
        return {
            "is_solved": self.engine.is_solved(),
            "facelets": self.engine.get_state(),
        }

    def reset_cube(self) -> Dict[str, Any]:
        self.engine.reset()
        return {
            "message": "Cube reset to standard solved state.",
            "facelets": self.engine.get_state(),
            "is_solved": True,
        }

    def scramble_cube(self, length: int = 20) -> Dict[str, Any]:
        moves = self.engine.scramble(length=length)
        return {
            "scramble_sequence": moves,
            "facelets": self.engine.get_state(),
            "is_solved": False,
        }

    def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        results = self.kb.query(query, top_k=2)
        return {
            "query": query,
            "results_count": len(results),
            "citations": [r["citation"] for r in results],
            "excerpts": [
                {
                    "title": r["title"],
                    "category": r["category"],
                    "content": r["content"],
                }
                for r in results
            ],
        }
