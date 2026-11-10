import json

INPUT_FILE = "knn/data/cleaned_jobs.jsonl"
NUMBER_OF_JOBS = 1000


def build_vectors():
    bow_vectors = []
    with open(INPUT_FILE, "r", encoding="utf-8") as input_file:
        for line in input_file:
            job = json.loads(line)
            word_counts = {}

            for word in job["description"].split():
                word_counts[word] = word_counts.get(word, 0) + 1

            bow_vectors.append(
                {
                    "id": job.get("id"),
                    "title": job.get("title"),
                    "location": job.get("location"),
                    "jobUrl": job.get("jobUrl"),
                    "word_counts": word_counts,
                }
            )

            if len(bow_vectors) == NUMBER_OF_JOBS:
                break

    return bow_vectors


if __name__ == "__main__":
    bow_vectors = build_vectors()
    print("Jobs:", len(bow_vectors))
