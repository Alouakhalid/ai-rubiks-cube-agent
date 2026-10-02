import random
from typing import List, Dict
from backend.app.cube.constants import (
    SOLVED_STATE,
    VALID_MOVES,
)


def _make_perm(cycles: List[List[int]]) -> List[int]:
    p = list(range(54))
    for cyc in cycles:
        for i in range(len(cyc)):
            p[cyc[(i + 1) % len(cyc)]] = cyc[i]
    return p


PERMS: Dict[str, List[int]] = {
    "U": _make_perm([
        [0, 2, 8, 6], [1, 5, 7, 3],
        [18, 36, 45, 9],
        [19, 37, 46, 10],
        [20, 38, 47, 11],
    ]),
    "D": _make_perm([
        [27, 29, 35, 33], [28, 32, 34, 30],
        [24, 15, 51, 42],
        [25, 16, 52, 43],
        [26, 17, 53, 44],
    ]),
    "F": _make_perm([
        [18, 20, 26, 24], [19, 23, 25, 21],
        [6, 9, 29, 44],
        [8, 15, 27, 38],
        [7, 12, 28, 41],
    ]),
    "B": _make_perm([
        [45, 47, 53, 51], [46, 50, 52, 48],
        [2, 36, 33, 17],
        [11, 0, 42, 35],
        [1, 39, 34, 14],
    ]),
    "L": _make_perm([
        [36, 38, 44, 42], [37, 41, 43, 39],
        [0, 18, 27, 53],
        [3, 21, 30, 50],
        [6, 24, 33, 47],
    ]),
    "R": _make_perm([
        [9, 11, 17, 15], [10, 14, 16, 12],
        [8, 45, 35, 26],
        [5, 48, 32, 23],
        [2, 51, 29, 20],
    ]),
}


class CubeEngine:
    def __init__(self, initial_state: str = SOLVED_STATE):
        self.state: str = initial_state if len(initial_state) == 54 else SOLVED_STATE
        self.move_history: List[str] = []
        self.scramble_history: List[str] = []

    def reset(self) -> None:
        self.state = SOLVED_STATE
        self.move_history.clear()
        self.scramble_history.clear()

    def get_state(self) -> str:
        return self.state

    def set_state(self, state: str) -> None:
        if len(state) == 54:
            self.state = state

    def is_solved(self) -> bool:
        for f in range(6):
            face_chars = self.state[f * 9 : (f + 1) * 9]
            if len(set(face_chars)) > 1:
                return False
        return True

    def apply_move(self, move: str) -> str:
        if move not in VALID_MOVES:
            return self.state

        base_move = move[0]
        perm = PERMS[base_move]

        repeat = 1
        if len(move) == 2 and move[1] == "2":
            repeat = 2
        elif len(move) == 2 and move[1] == "'":
            repeat = 3

        s = self.state
        for _ in range(repeat):
            s = "".join(s[perm[i]] for i in range(54))

        self.state = s
        self.move_history.append(move)
        return self.state

    def apply_moves(self, moves: List[str]) -> str:
        for m in moves:
            self.apply_move(m)
        return self.state

    def scramble(self, length: int = 20) -> List[str]:
        moves_pool = ["U", "D", "L", "R", "F", "B"]
        suffixes = ["", "'", "2"]
        scramble_moves: List[str] = []
        last_face = ""

        for _ in range(length):
            face = random.choice([f for f in moves_pool if f != last_face])
            suffix = random.choice(suffixes)
            m = f"{face}{suffix}"
            scramble_moves.append(m)
            last_face = face

        self.move_history.clear()
        self.scramble_history.clear()
        self.apply_moves(scramble_moves)
        self.scramble_history.extend(scramble_moves)
        return scramble_moves
