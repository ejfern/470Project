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

def find_jobs(user_query, jobs, selected_locations=None):
    if selected_locations:
        jobs = [job for job in jobs if job.get("location") in selected_locations]
    if not jobs:
        return []

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

    locations = set()
    for job in jobs:
        location = job.get("location")
        if location:
            locations.add(location.strip())
    locations = sorted(locations)
    selected_locations = set()

    location_search = ft.TextField(label="Search locations", hint_text="Type to filter")
    location_options = ft.Column(spacing=0)
    location_picker = ft.Container(
        content=ft.Column([
            location_search,
            ft.Row([
                ft.TextButton("Select all", on_click=lambda e: select_all_locations()),
                ft.TextButton("Clear", on_click=lambda e: clear_locations()),
            ]),
            location_options,
        ], tight=True),
        visible=False,
        padding=10,
    )
    location_button = ft.OutlinedButton("Locations (all)", on_click=lambda e: toggle_location_picker())

    def update_location_button():
        location_button.text = (
            f"Locations ({len(selected_locations)} selected)"
            if selected_locations else "Locations (all)"
        )

    def show_location_options(e=None):
        search_text = (location_search.value or "").strip().lower()
        location_options.controls.clear()
        for location in locations:
            if search_text and search_text not in location.lower():
                continue

            def on_location_change(e, location=location):
                if e.control.value:
                    selected_locations.add(location)
                else:
                    selected_locations.discard(location)
                update_location_button()
                page.update()

            location_options.controls.append(ft.Checkbox(
                label=location,
                value=location in selected_locations,
                on_change=on_location_change,
            ))
        page.update()

    location_search.on_change = show_location_options

    def select_all_locations():
        selected_locations.update(locations)
        show_location_options()
        update_location_button()

    def clear_locations():
        selected_locations.clear()
        show_location_options()
        update_location_button()

    def toggle_location_picker():
        location_picker.visible = not location_picker.visible
        if location_picker.visible:
            show_location_options()
        else:
            page.update()

    # search button functionality
    def search_jobs(e):
        # get user query (list of skills ex. "python, sql")
        user_query = query_input.value or ""

        # not query entered
        if not user_query.strip():
            return

        # run algorithm
        results = find_jobs(user_query, jobs, selected_locations)

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
                            "Skill-Based Job Search",
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
                
                location_button,

                ft.Button(
                    content = "Search Jobs",
                    on_click = search_jobs,
                    style = ft.ButtonStyle(
                        bgcolor = ft.Colors.GREY,
                        color = ft.Colors.PURPLE
                    )
                )
            ]),

            location_picker,

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
