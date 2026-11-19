This is the Requirement-Based Job Search Engine project

algorithm.py

run python3 algorithm.py "skill1, skill2, skill3"

uses functions from knn/build_vectors.py, vsm.py, and cosine_similarity.py

info retreival and ranking function that takes a list of job dictionaries, takes each job description and transforms it into a plain text string to be weighted using VSM. the then weighted job vector is compared against user query vector to find a similarity score using cosine similarity. score is used to rank job based on relevance to user's skills.