from collections import Counter
from typing import Dict, Any, List
from backend.app.cube.constants import (
    FACES,
    CORNER_FACELETS,
    EDGE_FACELETS,
)
from backend.app.cube.models import ValidationResult


class CubeValidator:
    @staticmethod
    def validate_state(state: str) -> ValidationResult:
        if not isinstance(state, str):
            return ValidationResult(
                is_valid=False,
                message="Cube state must be a string.",
            )

        if len(state) != 54:
            return ValidationResult(
                is_valid=False,
                message=f"Cube state must contain exactly 54 stickers, got {len(state)}.",
            )

        counts = Counter(state)
        for face in FACES:
            if counts.get(face, 0) != 9:
                return ValidationResult(
                    is_valid=False,
                    message=f"Face '{face}' has {counts.get(face, 0)} stickers (expected 9).",
                    details={"counts": dict(counts)},
                )

        center_indices = [4, 13, 22, 31, 40, 49]
        centers = [state[i] for i in center_indices]
        if len(set(centers)) != 6:
            return ValidationResult(
                is_valid=False,
                message="Center stickers must all be distinct.",
                details={"centers": centers},
            )

        for corner in CORNER_FACELETS:
            colors = [state[i] for i in corner]
            if len(set(colors)) != 3:
                return ValidationResult(
                    is_valid=False,
                    message="Corner piece contains duplicate colors.",
                    details={"corner_indices": corner, "colors": colors},
                )

        for edge in EDGE_FACELETS:
            colors = [state[i] for i in edge]
            if len(set(colors)) != 2:
                return ValidationResult(
                    is_valid=False,
                    message="Edge piece contains duplicate colors.",
                    details={"edge_indices": edge, "colors": colors},
                )

        return ValidationResult(
            is_valid=True,
            message="Cube state is physically valid.",
            details={"counts": dict(counts)},
        )
