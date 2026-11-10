Bag-of-Words KNN

This directory contains the preprocessing and retrieval pipeline for the
bag-of-words KNN baseline. 

Preprocessing

The preprocessing stage keeps useful job information, removes HTML from each
description, makes the text lowercase, removes extra spaces, and writes one
job per line to `data/cleaned_jobs.jsonl`.

Run the preprocessing from the `470Project` directory:

python3 -m knn.preprocess

Dictionary-based bag-of-words generation consumes the JSONL output in the next
pipeline stage.

Build a list of dictionary-based bag-of-words vectors for the first 1,000
cleaned jobs:

python3 -m knn.build_vectors

Enter a query and display the five closest jobs:

python3 -m knn.search

Run three small example queries:

python3 -m knn.demo
