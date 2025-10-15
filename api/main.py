from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .pyreval_stub import analyze_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Payload(BaseModel):
    claim: str = ""
    evidence: str = ""
    reasoning: str = ""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/analyze")
def analyze(payload: Payload):
    return analyze_text(payload.claim, payload.evidence, payload.reasoning)
