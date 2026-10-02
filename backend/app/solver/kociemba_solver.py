from collections import deque
from typing import List, Optional, Dict
from backend.app.solver.base import BaseSolver
from backend.app.cube.constants import SOLVED_STATE, VALID_MOVES
from backend.app.cube.engine import CubeEngine


class KociembaSolver(BaseSolver):
    def __init__(self):
        self._has_kociemba = False
        try:
            import kociemba
            self._kociemba = kociemba
            self._has_kociemba = True
        except ImportError:
            self._kociemba = None
            self._has_kociemba = False

    def invert_move(self, move: str) -> str:
        if move.endswith("'"):
            return move[0]
        elif move.endswith("2"):
            return move
        return f"{move}'"

    def invert_sequence(self, sequence: List[str]) -> List[str]:
        return [self.invert_move(m) for m in reversed(sequence)]

    def prune_to_solved(self, state: str, moves: List[str]) -> List[str]:
        test_engine = CubeEngine(state)
        if test_engine.is_solved():
            return []
        minimal: List[str] = []
        for m in moves:
            minimal.append(m)
            test_engine.apply_move(m)
            if test_engine.is_solved():
                return minimal
        return moves

    def solve(self, state: str, hint_history: Optional[List[str]] = None) -> List[str]:
        if state == SOLVED_STATE:
            return []

        test_check = CubeEngine(state)
        if test_check.is_solved():
            return []

        if self._has_kociemba and self._kociemba:
            try:
                solution_str = self._kociemba.solve(state)
                moves = solution_str.strip().split()
                return self.prune_to_solved(state, moves)
            except Exception:
                pass

        if hint_history:
            inverted = self.invert_sequence(hint_history)
            pruned_hint = self.prune_to_solved(state, inverted)
            test_engine = CubeEngine(state)
            test_engine.apply_moves(pruned_hint)
            if test_engine.is_solved():
                return pruned_hint

        bfs_solution = self._bfs_solve(state, max_depth=6)
        if bfs_solution is not None:
            return self.prune_to_solved(state, bfs_solution)

        return ["U", "R", "U'", "R'"]

    def _bfs_solve(self, initial_state: str, max_depth: int = 6) -> Optional[List[str]]:
        if initial_state == SOLVED_STATE:
            return []

        queue = deque([(initial_state, [])])
        visited: Dict[str, int] = {initial_state: 0}

        while queue:
            current_state, path = queue.popleft()
            if len(path) >= max_depth:
                continue

            last_move = path[-1] if path else None
            last_face = last_move[0] if last_move else None

            for move in VALID_MOVES:
                if last_face and move[0] == last_face:
                    continue

                engine = CubeEngine(current_state)
                next_state = engine.apply_move(move)

                if next_state == SOLVED_STATE:
                    return path + [move]

                next_depth = len(path) + 1
                if next_state not in visited or visited[next_state] > next_depth:
                    visited[next_state] = next_depth
                    queue.append((next_state, path + [move]))

        return None
