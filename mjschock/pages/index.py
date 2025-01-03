"""The home page of the app."""

import reflex as rx

from mjschock import styles
from mjschock.templates import template


@template(route="/", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()

    return rx.markdown(content, component_map=styles.markdown_style)
