import sys
import flet as ft

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


def main(page: ft.Page):
    page.title = "Skill-Based Job Search"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 600
    page.window_resizable = True
    page.padding = 20

    # input field for user query
    query_input = ft.TextField(
        label = "Skills",
        hint_text = "Enter skills, ex. \"python, sql\"",
        color = ft.Colors.PURPLE,
    )

    results_list = ft.ListView(
        spacing = 10,
        padding = 20,
        expand= True
    )

    # list of job dicts; cleaned
    # word_counts = bag of words in description
    jobs = build_vectors()

    # search button functionality
    def search_jobs(e):
        # get user query (list of skills ex. "python, sql")
        user_query = query_input.value or ""

        # not query entered
        if not user_query.strip():
            return

        # run algorithm
        results = find_jobs(user_query, jobs)

        # clear old results
        results_list.controls.clear()

        if not results:
            print("No matches.")
            return
        else:
            # ranked output (top 10 as specific in cosine_similarity.py)
            for (score, job) in results:
                results_list.controls.append(
                    ft.Text(
                        f"{job['title']} | {job.get('location')} | {job.get('jobUrl')} | Score: {float(score):.3f}"
                    )
                )
        page.update()

    page.add(
        ft.Column([
            ft.Container(
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls = [
                        ft.Text(
                            "NAME",
                            color = ft.Colors.BLACK,
                            size = 18,
                            weight = ft.FontWeight.BOLD,
                            font_family = "Arial"
                        ),
                        ft.Text(
                            "Right",
                            color = ft.Colors.BLACK,
                            size = 16,
                            font_family= "Arial"
                        ),
                    ]                
                ),
                border = ft.Border.all(2, ft.Colors.GREY),
                border_radius= 1,
                padding= 0,
            ),

            ft.Text(
                "Skill-Based Job Search",
                size = 20,
                weight = ft.FontWeight.BOLD,
                text_align = ft.TextAlign.CENTER,
                color = ft.Colors.BLUE
            ),
            ft.Row([
                query_input,
                
                ft.Divider(height = 20),

                ft.Button(
                    content = "Search Jobs",
                    on_click = search_jobs,
                    style = ft.ButtonStyle(
                        bgcolor = ft.Colors.GREY,
                        color = ft.Colors.PURPLE
                    )
                )
            ]),

            ft.Divider(height = 20),

            ft.Container(
                margin = 10,
                padding = 10,
                alignment = ft.Alignment.CENTER,
                bgcolor= ft.Colors.AMBER,
                border_radius = 10,

                # display results of algorithm
                content = results_list
            ),
            
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll = ft.ScrollMode.AUTO,
        spacing = 0,
        )
    )

    # if not results:
    #     print("No matches.")
    #     return

    # # ranked output (top 10 as specific in cosine_similarity.py)
    # for (score, job) in results:
    #     print(job['title'])
    #     print(" ", job.get("location"))
    #     print(" ", job.get("jobUrl"))
    #     print(" Score:", round(float(score), 3))

if __name__ == "__main__":
    ft.run(main)