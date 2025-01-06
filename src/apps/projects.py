import asyncio
import json
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
        self.flash_task = None
        self.flash_count = 0
        self.storage_key = "pomodoro_projects"

    async def did_mount(self):
        # Load saved projects when the component mounts
        await self.load_projects()

    async def save_projects(self):
        """Save project names to local storage"""
        project_names = [field.value for field in self.project_fields]
        projects_json = json.dumps(project_names)
        await self.page.client_storage.set_async(self.storage_key, projects_json)

    async def load_projects(self):
        """Load project names from local storage"""
        projects_json = await self.page.client_storage.get_async(self.storage_key)
        if projects_json:
            try:
                project_names = json.loads(projects_json)
                for field, name in zip(self.project_fields, project_names):
                    field.value = name
                self.update()
            except json.JSONDecodeError:
                print("Error loading saved projects")

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
                on_change=self.handle_project_change,
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

        # Create alert banner
        self.alert_banner = ft.Container(
            content=ft.Text(
                "Time's up! Take a break!",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
            ),
            bgcolor=ft.colors.RED_400,
            padding=20,
            visible=False,
            border_radius=5,
            alignment=ft.alignment.center,
        )

        # Create clear all button
        self.clear_button = ft.ElevatedButton(
            text="Clear All",
            on_click=self.clear_all_projects,
            icon=ft.icons.CLEAR_ALL,
        )

        # Main layout
        return ft.Container(
            content=ft.Column(
                [
                    self.alert_banner,
                    ft.Row(
                        [
                            ft.Text("Projects", size=32, weight=ft.FontWeight.BOLD),
                            self.clear_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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

    async def handle_project_change(self, e):
        """Handle changes to project text fields"""
        await self.save_projects()

    async def clear_all_projects(self, e):
        """Clear all project fields and storage"""
        for field in self.project_fields:
            field.value = ""
        await self.save_projects()
        self.update()

    def reset_colors(self):
        for container in self.project_rows:
            container.bgcolor = ft.colors.WHITE
        self.alert_banner.visible = False
        self.update()

    def reset_timer(self):
        if self.timer_project:
            self.timer_project.cancel()
            self.timer_project = None
        if self.flash_task:
            self.flash_task.cancel()
            self.flash_task = None

        self.timer_running = False
        self.remaining_time = 0
        self.timer_text.value = "25:00"
        self.start_timer_button.text = "Start Pomodoro"
        self.alert_banner.visible = False
        self.flash_count = 0

    async def flash_alert(self):
        while self.flash_count < 6:  # Flash 3 times (6 color changes)
            self.alert_banner.visible = True
            if self.flash_count % 2 == 0:
                self.alert_banner.bgcolor = ft.colors.RED_400
            else:
                self.alert_banner.bgcolor = ft.colors.ORANGE_400
            self.flash_count += 1
            self.update()
            await asyncio.sleep(0.5)

        self.alert_banner.visible = True
        self.alert_banner.bgcolor = ft.colors.RED_400

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
            # Start the flashing alert
            self.flash_task = asyncio.create_task(self.flash_alert())

            # Play a notification sound using the page's window object
            await self.page.window_to_front_async()
            await self.page.window_flash_async()

            self.timer_running = False
            self.start_timer_button.text = "Start Pomodoro"
            self.update()

    async def start_pomodoro(self, e):
        if not self.timer_running:
            self.timer_running = True
            self.remaining_time = 25 * 60  # 25 minutes in seconds
            self.start_timer_button.text = "Stop"
            self.alert_banner.visible = False
            # Create and store the timer project
            self.timer_project = asyncio.create_task(self.update_timer())
        else:
            self.reset_timer()

        self.update()


async def main(page: ft.Page):
    page.title = "Projects"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    await page.add_async(ProjectList())
