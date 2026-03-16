from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import re

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load inverted index
with open("inverted_index.json", "r") as f:
    inverted_index = json.load(f)

# Load IDF values
with open("idf.json", "r") as f:
    idf = json.load(f)

#tokenization
def tokenize_query(query):
    query = query.lower()
    query = re.sub(r"[^\w\s]", "", query)
    return query.split()

#ranking Documents
def rank_documents(tokens):
    scores = {}
    for token in tokens:
        if token not in inverted_index:
            continue
        postings = inverted_index[token]
        token_idf = idf.get(token, 0)
        for doc_id, tf in postings:
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += tf * token_idf
    return scores

#sorting according to scores
def sort_results(scores, top_n=13):
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]

@app.get("/")
def home():
    return  "Search Engine Backend is Running Successfully"

@app.get("/search")
def search(query: str):

    tokens = tokenize_query(query)

    scores = rank_documents(tokens)

    ranked_results = sort_results(scores)

    return {
        "query": query,
        "tokens": tokens,
        "results": ranked_results
    }