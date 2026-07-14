from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Fit the vectorizer on both texts together as a list

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def keyword_score(resume_text, job_description):
    vectorizer = TfidfVectorizer()
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
    resume_vector = model.encode(resume_text)
    jd_vector = model.encode(job_description)
    score = cosine_similarity([resume_vector], [jd_vector])
    return float(score[0][0])