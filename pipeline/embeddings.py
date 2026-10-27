from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

VEC_PATH = "data/tfidf.pkl"

def build(df):
    docs = df.apply(
        lambda r: f"{r.date} {r.category} {r.amount} Risk:{r.risk_tag}",
        axis=1
    ).tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(docs)

    with open(VEC_PATH, "wb") as f:
        pickle.dump((vectorizer, vectors, docs), f)

def retrieve(query, k=5):
    if not os.path.exists(VEC_PATH):
        return ""

    with open(VEC_PATH, "rb") as f:
        vectorizer, vectors, docs = pickle.load(f)

    qv = vectorizer.transform([query])
    sims = cosine_similarity(qv, vectors)[0]
    top = sims.argsort()[-k:][::-1]

    return "\n".join(docs[i] for i in top)
