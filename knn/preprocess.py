import html
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "ashby-jobs-with-descriptions.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "data" / "cleaned_jobs.jsonl"


def clean_description(description):
    description = re.sub(r"<[^>]+>", " ", description)
    description = html.unescape(description)
    return " ".join(description.lower().split())


def preprocess():
    with open(INPUT_FILE, "r", encoding="utf-8") as input_file:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
            for line in input_file:
                line = line.strip()

                if line in ("[", "]"):
                    continue

                if line.endswith(","):
                    line = line[:-1]

                job = json.loads(line)
                description = clean_description(job.get("descriptionHtml", ""))

                if not description:
                    continue

                job["description"] = description
                del job["descriptionHtml"]
                output_file.write(json.dumps(job) + "\n")


if __name__ == "__main__":
    preprocess()
