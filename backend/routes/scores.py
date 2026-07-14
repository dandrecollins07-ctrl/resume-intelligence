from pydantic import BaseModel
from fastapi import APIRouter, Depends, UploadFile, File, Form
from pdfminer.high_level import extract_text
import io
from collections import Counter
from services.scorer import keyword_score
from services.scorer import semantic_score
from database import SessionLocal
from models import Submission
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from sqlalchemy import func

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
        semantic_score=semantic_result,
        missing_skills=keyword_result["missing_keywords"]
    )
    db.add(submission)
    db.commit()
    db.close()

    return {"keyword": keyword_result, "semantic": semantic_result}

@router.get("/analytics")
def get_analytics():
    db = SessionLocal()
    day = func.date_trunc('day', Submission.created_at)
    trend = db.query(
        day.label("day"),
        func.avg(Submission.keyword_score),
        func.avg(Submission.semantic_score)
    ).group_by(day).order_by(day).all()
    trend_data = []
    for day, avg_kw, avg_sem in trend:
        trend_data.append({
            "day": day.strftime("%Y-%m-%d"),
            "avg_kw": avg_kw,
            "avg_sem": avg_sem,
        })

    all_missing = db.query(Submission.missing_skills).all()
    counter = Counter()
    for (skills,) in all_missing:
        if skills:
            counter.update(skills)
    top_missing = [{"skill": s, "count": c} for s, c in counter.most_common(10)]

    db.close()
    return {"score_trend": trend_data, "top_missing_skills": top_missing}