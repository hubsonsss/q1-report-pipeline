import argparse
import json
from pathlib import Path

from pipeline.extract import read_chart, read_markdown, read_pdf
from pipeline.report import build_findings, build_report


def main():
    parser = argparse.ArgumentParser(description="Q1 report pipeline")
    parser.add_argument("input_dir")
    parser.add_argument("-o", "--output", default="out")
    args = parser.parse_args()

    inp = Path(args.input_dir)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    print("Reading PDF...")
    pdf = read_pdf(inp / "Q1_2026_operations_report.pdf")
    print("Reading chart...")
    chart = read_chart(inp / "Q1_2026_capacity_chart.png")
    print("Reading notes...")
    notes = read_markdown(inp / "ops_notes_Q1_2026.md")

    print("Writing report...")
    report = build_report(pdf, chart, notes)
    (out / "report.md").write_text(report, encoding="utf-8")

    findings = build_findings(report)
    (out / "findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print(f"Done. Output in {out}/")


if __name__ == "__main__":
    main()
