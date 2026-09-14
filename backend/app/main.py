from __future__ import annotations

import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import config
from .memory_service import forget, improve, ingest_sample_chunks, recall, remember


@asynccontextmanager
async def lifespan(_: FastAPI):
    # No network connections are created here. Cognee databases are local.
    yield


app = FastAPI(
    title="Private Cognee Memory API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan,
)

# Only the local Node frontend is allowed by browser CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["content-type", "x-api-key"],
)


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key or not secrets.compare_digest(x_api_key, config.BACKEND_API_TOKEN):
        raise HTTPException(status_code=401, detail="Unauthorized")


class RememberRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)


class RecallRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=15)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/memory/ingest-sample", dependencies=[Depends(require_api_key)])
async def ingest_sample_endpoint():
    try:
        return await ingest_sample_chunks()
    except Exception as exc:
        # Do not return Cognee/provider/database exception details to clients.
        raise HTTPException(status_code=500, detail="Sample ingestion failed") from exc


@app.post("/memory/remember", dependencies=[Depends(require_api_key)])
async def remember_endpoint(request: RememberRequest):
    try:
        return await remember(request.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Memory write failed") from exc


@app.post("/memory/recall", dependencies=[Depends(require_api_key)])
async def recall_endpoint(request: RecallRequest):
    try:
        result = await recall(request.query, request.top_k)
        print("RECALL RESULT:", repr(result))
        return {"results": result}
    except Exception as exc:
        import traceback
        print("\n========== RECALL ERROR ==========")
        traceback.print_exc()
        print("==================================\n")
        raise HTTPException(
            status_code=500,
            detail=f"Memory recall failed: {type(exc).__name__}: {exc}"
        ) from exc


@app.post("/memory/improve", dependencies=[Depends(require_api_key)])
async def improve_endpoint():
    try:
        return await improve()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Memory improve failed") from exc


@app.post("/memory/forget", dependencies=[Depends(require_api_key)])
async def forget_endpoint():
    try:
        return await forget()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Memory deletion failed") from exc
