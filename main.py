from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from chains import rewrite_with_persona, multi_rewrite, debate

app = FastAPI()


# =========================
# SINGLE REWRITE
# =========================
class RewriteRequest(BaseModel):
    text: str
    persona: str


@app.post("/rewrite")
def rewrite_endpoint(body: RewriteRequest):
    result = rewrite_with_persona(body.text, body.persona)
    return {"output": result}


# =========================
# MULTI REWRITE
# =========================
class MultiRewriteRequest(BaseModel):
    text: str
    personas: List[str]


@app.post("/multi-rewrite")
def multi_rewrite_endpoint(body: MultiRewriteRequest):
    result = multi_rewrite(body.text, body.personas)
    return result


# =========================
# DEBATE WITH MEMORY
# =========================
class DebateRequest(BaseModel):
    topic: str
    personas: List[str]
    debate_id: Optional[str] = None


@app.post("/debate")
def debate_endpoint(body: DebateRequest):

    if len(body.personas) != 2:
        return {"error": "Exactly 2 personas required"}

    result = debate(
        body.topic,
        body.personas[0],
        body.personas[1],
        body.debate_id
    )

    return result
