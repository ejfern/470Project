# cosine similarity from scikit-learn library
from sklearn.metrics.pairwise import cosine_similarity

'''
notes: query_vector, job_vectors, job_ids to come from tf-idf implementation
or other preprocessing
'''

# calculate cosine similarity btwn query and all jobs
def calculate_similarity(query_vector, job_vectors):
    # vector of scores
    scores = cosine_similarity(query_vector, job_vectors)[0]

    return scores

# sort jobs from high to low similarity
# job_ids = list of job ids from json
# scores = list of cosine similarity scores from above
def rank_jobs(job_ids, scores):
    # zip job ids and similarity scores to each other respectively
    results = list(zip(job_ids, scores))

    # sort by similarity score
    results.sort(key = lambda x: x[1], reverse = True)

    # return top 10 jobs (CHANGE LATER??)
    return results[:10]

# calls cosine similarity and rank for top (10) jobs
def search(query_vector, job_vectors, job_ids):
    scores = calculate_similarity(
        query_vector,
        job_vectors
    )

    ranked_results = rank_jobs(
        job_ids,
        scores,
    )

    return ranked_results