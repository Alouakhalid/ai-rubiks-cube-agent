from typing import Dict
from backend.app.cube.engine import CubeEngine


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, CubeEngine] = {}

    def get_session(self, session_id: str = "default") -> CubeEngine:
        if session_id not in self.sessions:
            self.sessions[session_id] = CubeEngine()
        return self.sessions[session_id]

    def reset_session(self, session_id: str = "default") -> CubeEngine:
        engine = self.get_session(session_id)
        engine.reset()
        return engine

    def delete_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]


session_manager = SessionManager()
