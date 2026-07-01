from pydantic import BaseModel
from fastapi import APIRouter, Depends
from services.scorer import keyword_score
from services.scorer import semantic_score
from database import SessionLocal
from models import Submission
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

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

@router.get("/analytics")
def analytic_grab(db: Session = Depends(get_db)):

    result = db.execute(text('''
                SELECT UNNEST(missing_skills) 
                AS skill, COUNT(*) FROM submissions 
                GROUP BY skill ORDER BY COUNT(*) 
                DESC LIMIT 10;'''))
    
    rows = result.fetchall()
    top_skills = []
    for row in rows:
        top_skills.append({"skill": row[0], "count": row[1]})


    
    avg_score = db.execute(text('''
                    SELECT role_type, AVG(keyword_score),
                    AVG(semantic_score) FROM submissions
                    GROUP BY role_type;'''))
    
    role_rows = avg_score.fetchall()
    role_scores = []
    for role in role_rows:
        role_scores.append({"role_type": role[0], "avg_keyword": role[1], "avg_semantic": role[2]})

    return {"top_skills": top_skills, "role_scores": role_scores}
