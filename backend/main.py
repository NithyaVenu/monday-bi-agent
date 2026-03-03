import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

# @app.post("/chat")
# async def chat(req: ChatRequest):
#     result = await run_agent(req.message, req.history)
#     return result

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        result = await run_agent(req.message, req.history)
        return result
    except Exception as e:
        traceback.print_exc()  # shows real error in terminal
        return {"answer": f"Backend error: {str(e)}", "trace": []}

@app.get("/health")
def health():
    return {"status": "ok"}