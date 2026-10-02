from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CubeState(BaseModel):
    facelets: str = Field(..., min_length=54, max_length=54)
    is_solved: bool
    move_history: List[str] = Field(default_factory=list)
    scramble_sequence: Optional[str] = None


class MoveRequest(BaseModel):
    move: str


class MoveSequenceRequest(BaseModel):
    moves: List[str]


class ScrambleRequest(BaseModel):
    length: int = Field(default=20, ge=1, le=100)


class SetFaceletsRequest(BaseModel):
    facelets: str = Field(..., min_length=54, max_length=54)


class ValidationResult(BaseModel):
    is_valid: bool
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class SolutionResponse(BaseModel):
    solution: List[str]
    move_count: int
    explanation: Optional[str] = None
