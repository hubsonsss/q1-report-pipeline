# Q1 Report Pipeline

Turns a folder of client files (PDF report, PNG chart, Markdown notes) into a bank-ready report.

## Setup

```
pip install -r requirements.txt
cp .env.example .env   # add your OpenRouter key
```

## Run

```
python run.py ./input -o ./out
```

Outputs `out/report.md` and `out/findings.json`. An example run is in `example_output/`
(generated with `openai/gpt-4o-mini`).

## Environment variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `LLM_MODEL` | model for the report (default `openai/gpt-4o-mini`) |

## Discussion

**AI dev stack.** I used Cursor with Claude for most of the code. Day to day I use GPT-4o and Claude.

**Model choice.** `gpt-4o-mini` for everything: it is cheap, fast and supports images, so one model
covers both the chart and the report. I did not hit free-tier limits because it is a paid model.

**Architecture.** Each file is extracted separately (pypdf for the PDF, a vision model for the
chart, plain read for Markdown), then everything goes into one prompt that writes the report, and
a second prompt turns the report into JSON. The extraction is deterministic except for the chart.

**The image.** The chart is sent to a vision model that returns the numbers as a table. The pipeline
verifies the values by summing the regional segments and comparing them with the monthly totals.

**Conflicting sources.** The prompt tells the model to put inconsistencies in the "Data Quality"
section. On the provided files the data was broadly consistent.

**Structured output.** The model is asked to return only JSON. Code fences are stripped before
parsing.

**Scale.** With 300 files the single prompt would exceed the context window. I would add chunking
and a merge step.

**Cost.** Every run prints a per-stage token breakdown; a run uses about 12k tokens. To halve the
cost I would cache the chart extraction.

**Error handling.** API calls are retried with exponential backoff on rate limits and timeouts.

**Time spent.** About 3.5 hours. Getting the PDF tables out cleanly took longer than expected.
