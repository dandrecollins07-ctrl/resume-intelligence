from sklearn.feature_extraction.text import TfidfVectorizer
from fastembed import TextEmbedding
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        _model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _model


def keyword_score(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform([resume_text, job_description])
    words = vectorizer.get_feature_names_out()
    resume = matrix.toarray()[0]
    jd = matrix.toarray()[1]

    missing_words = [word for i, word in enumerate(words) if jd[i] > 0 and resume[i] == 0]

    jd_words = [word for i, word in enumerate(words) if jd[i] > 0]
    match_percent = (len(jd_words) - len(missing_words)) / len(jd_words) * 100
    return {"match_percent": match_percent, "missing_keywords": missing_words}


def semantic_score(resume_text, job_description):
    model = get_model()
    embeddings = list(model.embed([resume_text, job_description]))
    resume_vec, jd_vec = embeddings[0], embeddings[1]
    score = np.dot(resume_vec, jd_vec) / (np.linalg.norm(resume_vec) * np.linalg.norm(jd_vec))
    return float(score)