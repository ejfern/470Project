import json
import numpy as np

from cosine_similarity import search

# test tf-idf values
test_query = np.array([
    [1.0, 1.0, 0.0, 0.0]
])

test_jobs = np.array([
    [1.0, 1.0, 0.0, 0.0],
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 1.0],
    [0.0, 1.0, 0.0, 0.0]
])

test_job_ids =  ["TEST001", "TEST002", "TEST003", "TEST004"]

results = search(test_query, test_jobs, test_job_ids)

print("\nTOP MATCHING JOBS:")

for test_job_ids, score in results:
    print(test_job_ids, round(float(score), 4))