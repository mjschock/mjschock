"""The resume page."""

from mjschock import styles
from mjschock.templates import template

import reflex as rx


@template(route="/resume", title="Resume")
def resume() -> rx.Component:
    """The resume page.

    Returns:
        The UI for the resume page.
    """
    # with open("data/inputs/RESUME.md", encoding="utf-8") as resume_md:
    #     content = resume_md.read()

    # with open("data/inputs/style.css", encoding="utf-8") as style_css:
    #     style_css_content = style_css.read()
    #     print('TODO; parse this style_css_content into a dictionary: ', style_css_content)

    #     style: rx.Style = {
    #         "html": {
    #             "font-size": "10px;"
    #         },
    #         "h1": {
    #             "font-size": "16px;"
    #         },
    #         "h2": {
    #             "font-size": "14px;"
    #         },
    #         "h3": {
    #             "font-size": "12px;"
    #         },
    #         "table": {
    #             "border-spacing": "0;",
    #             "width": "100%;"
    #         },
    #         "th": {
    #             "font-size": "12px;"
    #         },
    #         "td:nth-child(even), th:nth-child(even)": {
    #             "text-align": "right;"
    #         },
    #         "ul": {
    #             "text-align": "justify;"
    #         }
    #     }

    # return rx.markdown(content, component_map=styles.markdown_style)
    # return rx.markdown(content, style=style)

    return rx.vstack(
        rx.heading("Resume", size="8"),
        # rx.text("Welcome to Reflex!"),
        # rx.text(
        #     "You can edit this page in ",
        #     rx.code("{your_app}/pages/resume.py"),
        # ),
        rx.html(
            "<embed src='/Resume - Michael James Schock.pdf' type='application/pdf' width='1024' height='768'>",
        )
    )

    # return rx.box(element="embed", src="/Resume.pdf", width="100%")
    # return rx.vstack(rx.image(src="/Resume.pdf"))
    # return rx.html(
    #     "<embed src='/Resume - Michael James Schock.pdf' type='application/pdf' width='100%'>"
    # )
