"""Find the five jobs most similar to a query."""

from knn.build_vectors import build_vectors


K = 5


def cosine_similarity(query_words, job_words):
    numerator = 0

    for word in query_words:
        numerator += query_words.get(word) * job_words.get(word, 0)

    query_sum = 0
    for word in query_words:
        query_sum += query_words.get(word) ** 2

    job_sum = 0
    for word in job_words:
        job_sum += job_words.get(word) ** 2

    denominator = (query_sum**0.5) * (job_sum**0.5)

    if denominator == 0:
        return 0

    return numerator / denominator


def search(query, jobs):
    query_words = {}

    for word in query.lower().split():
        query_words[word] = query_words.get(word, 0) + 1

    results = []

    for job in jobs:
        score = cosine_similarity(query_words, job["word_counts"])
        results.append((score, job))

    results.sort(key=lambda result: result[0], reverse=True)
    return results[:K]


def main():
    jobs = build_vectors()
    query = input("Enter a job search: ")
    results = search(query, jobs)

    for score, job in results:
        print()
        print(job["title"])
        print(job["location"])
        print(job["jobUrl"])
        print("Score:", round(score, 4))


if __name__ == "__main__":
    main()
