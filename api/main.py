from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
    # Basic CER evaluation stub
    cer = {
        "claim": bool(payload.claim.strip()),
        "evidence": bool(payload.evidence.strip()),
        "reasoning": bool(payload.reasoning.strip()),
    }

    hits = []
    gaps = []
    nudges = []
    trace = []

    if cer["claim"]:
        hits.append({"id": "claim-present", "label": "Claim Present", "weight": 5})
        trace.append({"cu": "claim-present", "span": payload.claim.strip()[:20]})
    else:
        gaps.append({"id": "claim-missing", "label": "Claim Missing", "weight": 5})
        nudges.append({"cu": "claim-missing", "text": "Please provide a scientific claim."})

    if cer["evidence"]:
        hits.append({"id": "evidence-present", "label": "Evidence Present", "weight": 3})
        trace.append({"cu": "evidence-present", "span": payload.evidence.strip()[:20]})
    else:
        gaps.append({"id": "evidence-missing", "label": "Evidence Missing", "weight": 3})
        nudges.append({"cu": "evidence-missing", "text": "Add data or examples supporting your claim."})

    if cer["reasoning"]:
        hits.append({"id": "reasoning-present", "label": "Reasoning Present", "weight": 2})
        trace.append({"cu": "reasoning-present", "span": payload.reasoning.strip()[:20]})
    else:
        gaps.append({"id": "reasoning-missing", "label": "Reasoning Missing", "weight": 2})
        nudges.append({"cu": "reasoning-missing", "text": "Explain how your evidence supports your claim."})

    return {
        "cer": cer,
        "hits": hits,
        "gaps": gaps,
        "nudges": nudges,
        "trace": trace,
    }
