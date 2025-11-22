import asyncio
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.agent_builder import build_agent

agent = build_agent()
app = FastAPI(title="ARES Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatReq(BaseModel):
    message: str
    model: Optional[str] = None
    temperature: float = 0.7


class ChatRes(BaseModel):
    response: str
    model: str


class SearchReq(BaseModel):
    query: str


class FileSearchRes(BaseModel):
    name: str
    path: str
    size: int
    modified: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/models", response_model=List[str])
def models():
    return agent.models()


@app.post("/chat", response_model=ChatRes)
async def chat(req: ChatReq):
    try:
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, agent.chat, req.message, req.model, req.temperature)
        return res
    except Exception as exc:
        return {"response": f"Errore server: {exc}", "model": req.model or ""}


@app.post("/search/files", response_model=List[FileSearchRes])
def search_files(req: SearchReq):
    return agent.search_files(req.query)


@app.post("/search/rag")
def search_rag(req: SearchReq):
    try:
        res = agent.rag_search(req.query)
        return {"answer": res}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/memory")
def memory():
    return {"history": agent.memory.history(limit=50)}


@app.delete("/memory")
def clear_memory():
    agent.memory.clear()
    return {"ok": True}


@app.get("/system")
def system():
    return agent.system_stats()
