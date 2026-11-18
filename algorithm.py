import sys

from knn.build_vectors import build_vectors 
from vsm import transform_vector
from cosine_similarity import search


def counts_to_text(word_counts):
    words = []
    for word, n in word_counts.items():
        # repeats word n times
        for _ in range(n):
            words.append(word)
    return " ".join(words)

def find_jobs(user_query, jobs):
    query = user_query.replace(",", " ").lower()

    job_texts = []
    for job in jobs:
        text = counts_to_text(job["word_counts"])
        job_texts.append(text)

    # vsm
    job_vectors, query_vector = transform_vector(job_texts, query)

    # cosine similarity
    ranked = search(query_vector, job_vectors, list(range(len(jobs))))

    results = []
    for i, score in ranked:
        if score > 0:
            # appends score w relevant job dict
            results.append((score, jobs[i]))
    return results


def main():
    # list of job dicts; cleaned
    # word_counts = bag of words in description
    jobs = build_vectors()

    # get user query (list of skills ex. "python, sql")
    user_query = " ".join(sys.argv[1:]) or input ("Enter your skills (comma separated): ")
    results = find_jobs(user_query, jobs)

    if not results:
        print("No matches.")
        return

    # ranked output (top 10 as specific in cosine_similarity.py)
    for (score, job) in results:
        print(job['title'])
        print(" ", job.get("location"))
        print(" ", job.get("jobUrl"))
        print(" Score:", round(float(score), 3))

if __name__ == "__main__":
    main()