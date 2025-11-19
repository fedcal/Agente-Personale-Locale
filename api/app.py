from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.agent_builder import build_agent
from rag.search import semantic_search
import asyncio

app = FastAPI(title="ARES Agent API")
agent = build_agent()

class ChatReq(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatReq):
    try:
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, agent.run, req.message)
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SearchReq(BaseModel):
    query: str

@app.post("/search")
async def search(req: SearchReq):
    try:
        res = semantic_search(req.query)
        return {"answer": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
