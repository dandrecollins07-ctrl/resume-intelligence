from sklearn.feature_extraction.text import TfidfVectorizer
from fastembed import TextEmbedding
import numpy as np

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