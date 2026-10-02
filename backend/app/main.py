import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.api.v1.cube_router import router as cube_router
from backend.app.api.v1.agent_router import router as agent_router
from backend.app.api.v1.ws_router import router as ws_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cube_router, prefix=settings.API_V1_STR)
app.include_router(agent_router, prefix=settings.API_V1_STR)
app.include_router(ws_router, prefix=settings.API_V1_STR)

STATIC_INDEX = os.path.join(os.path.dirname(__file__), "static", "index.html")


@app.get("/")
def serve_index():
    if os.path.exists(STATIC_INDEX):
        return FileResponse(STATIC_INDEX)
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
