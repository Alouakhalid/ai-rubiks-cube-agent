from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from backend.app.services.session_manager import session_manager
from backend.app.cube.models import (
    CubeState,
    MoveRequest,
    MoveSequenceRequest,
    ScrambleRequest,
    SetFaceletsRequest,
    ValidationResult,
)
from backend.app.cube.validator import CubeValidator
from backend.app.rag.knowledge_base import knowledge_base

router = APIRouter(prefix="/cube", tags=["Cube"])


@router.get("/state", response_model=CubeState)
def get_state(session_id: str = "default") -> CubeState:
    engine = session_manager.get_session(session_id)
    return CubeState(
        facelets=engine.get_state(),
        is_solved=engine.is_solved(),
        move_history=engine.move_history,
        scramble_sequence=" ".join(engine.scramble_history) if engine.scramble_history else None,
    )


@router.post("/reset", response_model=CubeState)
def reset_cube(session_id: str = "default") -> CubeState:
    engine = session_manager.reset_session(session_id)
    return CubeState(
        facelets=engine.get_state(),
        is_solved=True,
        move_history=[],
        scramble_sequence=None,
    )


@router.post("/scramble")
def scramble_cube(req: ScrambleRequest, session_id: str = "default") -> Dict[str, Any]:
    engine = session_manager.get_session(session_id)
    moves = engine.scramble(length=req.length)
    return {
        "scramble": moves,
        "scramble_string": " ".join(moves),
        "state": engine.get_state(),
        "is_solved": engine.is_solved(),
    }


@router.post("/move", response_model=CubeState)
def make_move(req: MoveRequest, session_id: str = "default") -> CubeState:
    engine = session_manager.get_session(session_id)
    engine.apply_move(req.move)
    return CubeState(
        facelets=engine.get_state(),
        is_solved=engine.is_solved(),
        move_history=engine.move_history,
    )


@router.post("/moves", response_model=CubeState)
def make_moves(req: MoveSequenceRequest, session_id: str = "default") -> CubeState:
    engine = session_manager.get_session(session_id)
    engine.apply_moves(req.moves)
    return CubeState(
        facelets=engine.get_state(),
        is_solved=engine.is_solved(),
        move_history=engine.move_history,
    )


@router.post("/set-state", response_model=CubeState)
def set_state(req: SetFaceletsRequest, session_id: str = "default") -> CubeState:
    val = CubeValidator.validate_state(req.facelets)
    if not val.is_valid:
        raise HTTPException(status_code=422, detail=val.message)

    engine = session_manager.get_session(session_id)
    engine.set_state(req.facelets)
    engine.move_history.clear()
    engine.scramble_history.clear()
    return CubeState(
        facelets=engine.get_state(),
        is_solved=engine.is_solved(),
        move_history=[],
    )


@router.post("/validate", response_model=ValidationResult)
def validate_cube(req: Optional[SetFaceletsRequest] = None, session_id: str = "default") -> ValidationResult:
    if req and req.facelets:
        return CubeValidator.validate_state(req.facelets)
    engine = session_manager.get_session(session_id)
    return CubeValidator.validate_state(engine.get_state())


@router.get("/knowledge")
def search_knowledge(q: str = Query(..., description="Query literature")) -> Dict[str, Any]:
    results = knowledge_base.query(q, top_k=3)
    return {
        "query": q,
        "count": len(results),
        "results": results,
    }
