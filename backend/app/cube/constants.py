from typing import Dict, List, Tuple

FACES: List[str] = ["U", "R", "F", "D", "L", "B"]

COLOR_MAP: Dict[str, str] = {
    "U": "white",
    "R": "red",
    "F": "green",
    "D": "yellow",
    "L": "orange",
    "B": "blue",
}

REVERSE_COLOR_MAP: Dict[str, str] = {v: k for k, v in COLOR_MAP.items()}

VALID_MOVES: List[str] = [
    "U", "U'", "U2",
    "D", "D'", "D2",
    "L", "L'", "L2",
    "R", "R'", "R2",
    "F", "F'", "F2",
    "B", "B'", "B2",
]

SOLVED_STATE: str = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

FACELET_OFFSETS: Dict[str, int] = {
    "U": 0,
    "R": 9,
    "F": 18,
    "D": 27,
    "L": 36,
    "B": 45,
}

CORNER_FACELETS: List[Tuple[int, int, int]] = [
    (8, 9, 20),
    (6, 18, 38),
    (0, 36, 47),
    (2, 45, 11),
    (29, 26, 15),
    (27, 44, 24),
    (33, 53, 42),
    (35, 17, 51),
]

EDGE_FACELETS: List[Tuple[int, int]] = [
    (5, 10),
    (7, 19),
    (3, 37),
    (1, 46),
    (32, 16),
    (28, 25),
    (30, 43),
    (34, 52),
    (23, 12),
    (21, 41),
    (50, 39),
    (48, 14),
]
