from pydantic import BaseModel
from fastapi import APIRouter, Depends, UploadFile, File, Form
from pdfminer.high_level import extract_text
import io
from services.scorer import keyword_score
from services.scorer import semantic_score
from database import SessionLocal
from models import Submission
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.post("/score")
def request_score(resume: UploadFile = File(...), job_description: str = Form(...)):
    resume_bytes = resume.file.read()
    resume_text = extract_text(io.BytesIO(resume_bytes))

    keyword_result = keyword_score(resume_text, job_description)
    semantic_result = semantic_score(resume_text, job_description)

    db = SessionLocal()
    submission = Submission(
        resume_text=resume_text,
        jd_text=job_description,
        keyword_score=keyword_result["match_percent"],
        semantic_score=semantic_result
    )
    db.add(submission)
    db.commit()
    db.close()

    return {"keyword": keyword_result, "semantic": semantic_result}