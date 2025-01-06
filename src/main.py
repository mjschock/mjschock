import os
from contextlib import asynccontextmanager

import flet as ft
import flet.fastapi as flet_fastapi
import uvicorn
from fastapi import FastAPI

from apps.projects import main as projects_main

cwd = os.getcwd()
print("cwd:", cwd)

data_dir = os.getenv("FLET_APP_STORAGE_DATA", f"{cwd}/storage/data")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


app = FastAPI(lifespan=lifespan)


async def root_main(page: ft.Page):
    # with open(f"{data_dir}/README.md") as f:
    with open(f"{data_dir}/resume.md") as f:
        md1 = f.read()

    page.scroll = "auto"

    await page.add_async(
        ft.Markdown(
            md1,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data),
        )
    )


app.mount("/projects", flet_fastapi.app(projects_main))
app.mount("/", flet_fastapi.app(root_main))


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
