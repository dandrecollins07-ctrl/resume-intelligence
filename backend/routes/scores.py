from pydantic import BaseModel
from fastapi import APIRouter
from services.scorer import keyword_score
from services.scorer import semantic_score
from database import SessionLocal
from models import Submission

class ScoreRequest(BaseModel):
    resume_text: str
    job_description: str

router = APIRouter()

@router.post("/score")
def request_score(request: ScoreRequest):
    keyword_result = keyword_score(request.resume_text, request.job_description)
    semantic_result = semantic_score(request.resume_text, request.job_description)

    db = SessionLocal()
    submission = Submission(
        resume_text=request.resume_text,
        jd_text=request.job_description,
        keyword_score=keyword_result["match_percent"],
        semantic_score=semantic_result
    )
    db.add(submission)
    db.commit()
    db.close()

    return {"keyword": keyword_result, "semantic": semantic_result}