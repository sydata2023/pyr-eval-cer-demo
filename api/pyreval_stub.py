from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ContentUnit:
    id: str
    label: str
    keywords: List[str]
    weight: int = 1
    nudge: str = ""

RUBRIC: List[ContentUnit] = [
    ContentUnit(
        id="CU1",
        label="Mitochondria as the cell's powerhouse",
        keywords=["mitochondria", "powerhouse", "energy"],
        weight=5,
        nudge="Explain why mitochondria are called the cell's powerhouse."
    ),
    ContentUnit(
        id="CU2",
        label="ATP production",
        keywords=["ATP", "adenosine triphosphate", "energy molecule"],
        weight=4,
        nudge="Describe how ATP is produced and used for cellular work."
    ),
    ContentUnit(
        id="CU3",
        label="Cellular respiration",
        keywords=["respiration", "glucose", "oxygen", "co2", "water"],
        weight=3,
        nudge="Mention the inputs and outputs of cellular respiration."
    ),
]

def analyze_text(claim: str, evidence: str, reasoning: str) -> Dict:
    full_text = f"{claim} {evidence} {reasoning}".lower()
    hits, gaps, nudges, trace = [], [], [], []
    for cu in RUBRIC:
        matched = [kw for kw in cu.keywords if kw.lower() in full_text]
        if matched:
            hits.append({"id": cu.id, "label": cu.label, "weight": cu.weight})
            trace.append({"cu": cu.id, "span": matched[0]})
        else:
            gaps.append({"id": cu.id, "label": cu.label, "weight": cu.weight})
            nudges.append({"cu": cu.id, "text": cu.nudge})
    cer = {
        "claim": bool(claim.strip()),
        "evidence": bool(evidence.strip()),
        "reasoning": bool(reasoning.strip()),
    }
    return {"cer": cer, "hits": hits, "gaps": gaps, "nudges": nudges, "trace": trace}
