from sklearn.feature_extraction.text import TfidfVectorizer
from fastembed import TextEmbedding
import numpy as np
from services.skills import extract_skills
from services.skill_taxonomy import classify_role

_model = None

def get_model():
    global _model
    if _model is None:
        _model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _model


def keyword_score(resume_text, job_description, corpus_jds):
    # Fit on the full JD history + resume, so IDF reflects real-world word rarity
    documents = corpus_jds + [resume_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(documents)
    words = vectorizer.get_feature_names_out()

    # current JD is the last item in corpus_jds; resume is the very last document
    jd_index = len(corpus_jds) - 1
    resume_index = len(documents) - 1

    dense = matrix.toarray()
    jd = dense[jd_index]
    resume = dense[resume_index]

    missing_words = [word for i, word in enumerate(words) if jd[i] > 0 and resume[i] == 0]

    jd_words = [word for i, word in enumerate(words) if jd[i] > 0]
    match_percent = (len(jd_words) - len(missing_words)) / len(jd_words) * 100 if jd_words else 0
    return {"match_percent": match_percent, "missing_keywords": missing_words}


def semantic_score(resume_text, job_description):
    model = get_model()
    embeddings = list(model.embed([resume_text, job_description]))
    resume_vec, jd_vec = embeddings[0], embeddings[1]
    score = np.dot(resume_vec, jd_vec) / (np.linalg.norm(resume_vec) * np.linalg.norm(jd_vec))
    return float(score)

def skill_gap(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)
    extra_skills = sorted(resume_skills - jd_skills)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
    }

def role_classification(resume_text, job_description):
    from services.skills import extract_skills
    jd_skills = extract_skills(job_description)
    return classify_role(jd_skills)