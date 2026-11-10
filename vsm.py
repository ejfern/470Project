#basic VSM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def transform_vector(jobs, query):
    vectorizer = TfidfVectorizer()
    job_vectors = vectorizer.fit_transform(jobs)
    query_vector = vectorizer.transform([query])
    return job_vectors, query_vector

def getSimilarityScore(query_vector, job_vector):
    similarities = cosine_similarity(query_vector, job_vector)[0]
    return similarities

def main():
    jobs = [
        "Software Engineer Python Java AWS backend development",
        "Data Scientist Python machine learning SQL statistics",
        "Frontend Engineer JavaScript React HTML CSS",
        "Backend Software Engineer Python Django REST APIs",
    ]

    query = "Python software engineer backend"
    job_vectors, query_vector = transform_vector(jobs, query)
    similarities = getSimilarityScore(query_vector, job_vectors)
    ranked_jobs = sorted(
        enumerate(similarities),
        key=lambda x: x[1],
        reverse=True
    )
    for index, score in ranked_jobs:
        print(f"Score: {score:.4f}")
        print(f"Job: {jobs[index]}")
        print()

if __name__ == "__main__":
    main()