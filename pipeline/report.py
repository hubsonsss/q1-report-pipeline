import json

from pipeline.llm import chat

REPORT_PROMPT = """You are preparing a Q1 2026 report for a solar installation company that is
applying for a bank loan. Below are three documents. Write a report in Markdown with these
sections: Executive Summary, Key Figures, Findings and Risks, Data Quality and Inconsistencies,
Recommended Actions.

In the Executive Summary write one paragraph summarizing each document.

## Operations report (PDF)
{pdf}

## Capacity chart (extracted)
{chart}

## Ops meeting notes
{notes}
"""

FINDINGS_PROMPT = """From the report below, return a JSON object with keys "key_figures" (object)
and "findings" (list of strings). Return only JSON.

{report}
"""


def build_report(pdf: str, chart: str, notes: str) -> str:
    return chat(REPORT_PROMPT.format(pdf=pdf, chart=chart, notes=notes))


def build_findings(report: str) -> dict:
    raw = chat(FINDINGS_PROMPT.format(report=report))
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(raw)
