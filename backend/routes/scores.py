from pydantic import BaseModel
from fastapi import FastAPI, APIRouter
from services.scorer import keyword_score
from services.scorer import semantic_score

class ScoreRequest(BaseModel):
    resume_text: str
    job_description: str

router = APIRouter()

@router.post("/score")
def request_score(request: ScoreRequest):
    return {"keyword": keyword_score(request.resume_text, request.job_description), "semantic": semantic_score(request.resume_text, request.job_description)}
