import os
from pathlib import Path

import markdown
import pypandoc
from weasyprint import CSS, HTML


class MarkdownConverter:
    def __init__(self, markdown_file: str):
        self.markdown_file = Path(markdown_file)
        if not self.markdown_file.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

        self.markdown_content = self.markdown_file.read_text()

    def to_html(self, output_file: str = None):
        """Convert markdown to HTML with styling"""
        if output_file is None:
            output_file = self.markdown_file.with_suffix(".html")

        # Convert markdown to HTML
        html_content = markdown.markdown(
            self.markdown_content, extensions=["tables", "fenced_code"]
        )

        # Add CSS styling
        css = """
        <style>
            body {
                font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 2rem;
                color: #333;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f5f5f5;
            }
            h1, h2, h3 { color: #2c3e50; }
            code {
                background-color: #f8f9fa;
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: Consolas, Monaco, 'Andale Mono', monospace;
            }
            pre {
                background-color: #f8f9fa;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
            }
            a { color: #3498db; }
            a:hover { text-decoration: underline; }
        </style>
        """

        html_content = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.markdown_file.stem}</title>
            {css}
        </head>
        <body>
            {html_content}
        </body>
        </html>"""

        Path(output_file).write_text(html_content)
        return output_file

    def to_pdf_pandoc(self, output_file: str = None):
        """Convert markdown to PDF using pandoc"""
        if output_file is None:
            output_file = self.markdown_file.with_suffix(".pdf")

        pypandoc.convert_file(
            str(self.markdown_file),
            "pdf",
            outputfile=str(output_file),
            extra_args=["--pdf-engine=xelatex", "-V", "geometry:margin=1in"],
        )
        return output_file

    def to_pdf_weasyprint(self, output_file: str = None):
        """Convert markdown to PDF using WeasyPrint"""
        if output_file is None:
            output_file = self.markdown_file.with_suffix(".pdf")

        html = markdown.markdown(
            self.markdown_content, extensions=["tables", "fenced_code"]
        )

        css = CSS(
            string="""
            @page { margin: 1in; }
            body { font-family: -apple-system, system-ui, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            code { background: #f8f9fa; padding: 0.2em 0.4em; }
        """
        )

        HTML(string=html).write_pdf(output_file, stylesheets=[css])
        return output_file

    def to_docx(self, output_file: str = None):
        """Convert markdown to DOCX using pandoc"""
        if output_file is None:
            output_file = self.markdown_file.with_suffix(".docx")

        pypandoc.convert_file(
            str(self.markdown_file), "docx", outputfile=str(output_file)
        )
        return output_file


# Example usage
if __name__ == "__main__":
    cwd = os.getcwd()
    data_dir = os.getenv("FLET_APP_STORAGE_DATA", f"{cwd}/storage/data")

    converter = MarkdownConverter(f"{data_dir}/resume.md")

    converter.to_pdf_pandoc(f"{data_dir}/resume_pandoc.pdf")
    converter.to_pdf_weasyprint(f"{data_dir}/resume_weasyprint.pdf")
    converter.to_docx(f"{data_dir}/resume.docx")
