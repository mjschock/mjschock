import asyncio
import random

import flet as ft


class ProjectList(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.max_items = 6
        self.selected_project_index = None
        self.timer_running = False
        self.remaining_time = 0
        self.timer_project = None

    def build(self):
        # Create project fields
        self.project_fields = []

        for i in range(self.max_items):
            field = ft.TextField(
                value=f"Project {i+1}",
                border=ft.InputBorder.UNDERLINE,
                color=ft.colors.BLACK,
                bgcolor=ft.colors.WHITE,
                expand=True,
            )

            self.project_fields.append(field)

        # Create project rows
        self.project_rows = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"{i+1}.", color=ft.colors.BLACK, size=16),
                        self.project_fields[i],
                    ]
                ),
                bgcolor=ft.colors.WHITE,
                padding=10,
                border_radius=5,
            )
            for i in range(self.max_items)
        ]

        # Create dice button and timer elements
        self.dice_button = ft.ElevatedButton(text="🎲", on_click=self.roll_dice)

        self.timer_text = ft.Text("25:00", size=24)
        self.start_timer_button = ft.ElevatedButton(
            text="Start Pomodoro", on_click=self.start_pomodoro, disabled=True
        )

        # Main layout
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [ft.Text("Projects", size=32, weight=ft.FontWeight.BOLD)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(self.project_rows, spacing=10),
                    ft.Row(
                        [self.dice_button, self.timer_text, self.start_timer_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            padding=20,
        )

    def reset_colors(self):
        for container in self.project_rows:
            container.bgcolor = ft.colors.WHITE
        self.update()

    def reset_timer(self):
        if self.timer_project:
            self.timer_project.cancel()
            self.timer_project = None

        self.timer_running = False
        self.remaining_time = 0
        self.timer_text.value = "25:00"
        self.start_timer_button.text = "Start Pomodoro"

    async def roll_dice(self, e):
        # Reset previous selection and timer
        self.reset_colors()
        self.reset_timer()

        # Get non-empty projects
        non_empty_projects = [
            (i, field)
            for i, field in enumerate(self.project_fields)
            if field.value.strip()
        ]

        if non_empty_projects:
            # Select random project
            self.selected_project_index, _ = random.choice(non_empty_projects)
            self.project_rows[self.selected_project_index].bgcolor = ft.colors.BLUE_100
            self.start_timer_button.disabled = False

        else:
            self.selected_project_index = None
            self.start_timer_button.disabled = True

        self.update()

    async def update_timer(self):
        while self.timer_running and self.remaining_time > 0:
            await asyncio.sleep(1)
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_text.value = f"{minutes:02d}:{seconds:02d}"
            self.update()

        if self.remaining_time <= 0:
            self.reset_timer()
            self.update()

    async def start_pomodoro(self, e):
        if not self.timer_running:
            self.timer_running = True
            self.remaining_time = 25 * 60  # 25 minutes in seconds
            self.start_timer_button.text = "Stop"
            # Create and store the timer project
            self.timer_project = asyncio.create_task(self.update_timer())

        else:
            self.reset_timer()

        self.update()


async def main(page: ft.Page):
    page.title = "Projects"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    await page.add_async(ProjectList())
