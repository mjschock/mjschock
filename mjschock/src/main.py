import os
import flet as ft

data_dir = os.getenv("FLET_APP_STORAGE_DATA")

# def main(page: ft.Page):
#     counter = ft.Text("0", size=50, data=0)

#     def increment_click(e):
#         counter.data += 1
#         counter.value = str(counter.data)
#         counter.update()

#     page.floating_action_button = ft.FloatingActionButton(
#         icon=ft.Icons.ADD, on_click=increment_click
#     )
#     page.add(
#         ft.SafeArea(
#             ft.Container(
#                 counter,
#                 alignment=ft.alignment.center,
#             ),
#             expand=True,
#         )
#     )

def main(page: ft.Page):
    # with open(f"{data_dir}/README.md") as f:
    with open(f"{data_dir}/resume.md") as f:
        md1 = f.read()

    page.scroll = "auto"
    page.add(
        ft.Markdown(
            md1,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data),
        )
    )


ft.app(main)
