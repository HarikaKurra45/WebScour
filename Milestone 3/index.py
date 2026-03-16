import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import math

# Task 1 – Load HTML Documents
PAGES_DIR = "pages"
documents = {}
doc_id = 1
for filename in os.listdir(PAGES_DIR):
    if filename.endswith(".html"):
        file_path = os.path.join(PAGES_DIR, filename)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            documents[doc_id] = f.read()
            doc_id += 1

total_docs = len(documents)

# Task 2 – Extract Visible Text
def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text()
    return text

clean_documents = {}

for doc_id, html in documents.items():
    clean_documents[doc_id] = extract_visible_text(html)

# Task 3 – Tokenization
def tokenize(text):
    text = text.lower()  
    text = re.sub(r"[^\w\s]", "", text)  
    words = text.split()  
    return words

tokenized_documents = {}

for doc_id, text in clean_documents.items():
    words = tokenize(text)
    tokenized_documents[doc_id] = words

with open("all_tokens.json", "w", encoding="utf-8") as f:
    json.dump(tokenized_documents, f, indent=4)

# Task 4 – Compute Term Frequency
term_frequencies = {}

for doc_id, words in tokenized_documents.items():
    tf = defaultdict(int)
    for word in words:
        tf[word] += 1

    term_frequencies[doc_id] = dict(tf)

with open("term_frequencies.json", "w", encoding="utf-8") as f:
    json.dump(term_frequencies, f, indent=4)

# Task 5 – Build Inverted Index
inverted_index = defaultdict(list)

for doc_id, tf_dict in term_frequencies.items():
    for word, freq in tf_dict.items():
        inverted_index[word].append((doc_id, freq))

# Task 6 – Save Inverted Index to Disk
inverted_index_dict = dict(inverted_index)

with open("inverted_index.json", "w", encoding="utf-8") as f:
    json.dump(inverted_index_dict, f, indent=4)

# Task 7 – Compute IDF
idf = {}
N = total_docs 
for word, postings in inverted_index.items():
    df = len(postings)  
    idf[word] = math.log(N / df)

# Task 8 – Save IDF to Disk
with open("idf.json", "w", encoding="utf-8") as f:
    json.dump(idf, f, indent=4)

# Task 9 – Validation
print("Number of documents indexed:", total_docs)

print("Number of unique terms:", len(inverted_index))

print("\nSample Tokens:\n")
sample_id = next(iter(tokenized_documents))
print(tokenized_documents[sample_id][:20])
print("All tokens saved to all_tokens.json")

print("\nSample Term Frequencies:")
count = 0
for doc_id, tf_dict in term_frequencies.items():
    print("Document ID:", doc_id)
    print(list(tf_dict.items())[:10])  
    count += 1
    if count == 7:   
        break
print("Term frequencies saved to term_frequencies.json")

print("\nSample Inverted Index Entries:")
count = 0
for word, postings in inverted_index.items():
    print(word, "->", postings)
    count += 1
    if count == 7:
        break
print("\nInverted index saved to inverted_index.json")

print("\nSample IDF Values:")
count = 0
for word, value in idf.items():
    print(word, "->", round(value, 4))
    count += 1
    if count == 7:
        break
print("\nIDF values saved to idf.json")
