from knn.build_vectors import build_vectors
from knn.search import search


queries = [
    "python software engineer",
    "machine learning",
    "product manager",
]

jobs = build_vectors()

for query in queries:
    print("\nQuery:", query)

    for score, job in search(query, jobs):
        print(round(score, 4), "-", job["title"])
