from pypdf import PdfReader

from pipeline.llm import describe_image


def read_pdf(path) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def read_markdown(path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_chart(path) -> str:
    return describe_image(
        str(path),
        "This is a chart from a solar installation company. "
        "Extract all the numbers from the chart (per month and per region) as a table.",
    )
