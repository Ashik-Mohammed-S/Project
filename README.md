# Retail Finance Evidence Copilot

[![CI](https://github.com/Ashik-Mohammed-S/Project/actions/workflows/ci.yml/badge.svg)](https://github.com/Ashik-Mohammed-S/Project/actions/workflows/ci.yml)

An independent applied-AI portfolio project connecting **retail finance, SQL
controls, evidence retrieval and evaluation**. Built around a fictional retailer,
Harbor Retail, with no employer, customer or patient data.

The business question: can a finance analyst inspect a metric or contract
exception, retrieve its definition and controls, and see exactly which evidence
an answer relies on?

**Current release:** runnable Flask app, 576 synthetic sales lines, three read-only
SQL reports, evidence quotations, retrieval/abstention evaluation and an optional
local Ollama generation adapter. This is not a Walgreens project, production
deployment or an employer-endorsed system.

## Try it

Use Python 3.14 (see .python-version):

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
waitress-serve --host=127.0.0.1 --port=8081 app:app
```

Open http://127.0.0.1:8081. Ask “How is gross margin rate calculated?” or
“How many below-floor lines are in the ledger?” Then inspect the source evidence.
The default is a retrieved quotation, **not generated prose**.

```sh
python -m unittest discover -s tests
python evaluate.py --check
```

## What is implemented

| Layer | Implementation | Why it matters |
| --- | --- | --- |
| Data | Seeded fictional ledger, integer cents, explicit grain and provenance | Reproducible finance calculations without employer data |
| SQL | Monthly margin, contract price gaps and data-quality reports | Inspectable business logic; no arbitrary text-to-SQL execution |
| Retrieval | SQLite FTS5 BM25 baseline; character-trigram rank fusion candidate | Compare a simple baseline before claiming a more complex method helps |
| Answering | Exact evidence quotation with source IDs and abstention threshold | Readers can inspect the evidence and unsupported requests |
| Optional generation | Local-only Ollama HTTP adapter with structured output checks | Separates model integration from tested retrieval behavior |
| Evaluation | 24 development cases, 24 separate authored test cases, committed results | Reproducible configuration selection and regression checks |
| API | Flask, bounded inputs, read-only reports, request IDs and elapsed time | Usable software beyond a notebook |

The synthetic price-floor query finds **8 injected exception lines** and a
**136,800-cent potential price gap**. These are properties of generated data,
not employer savings or business impact.

## Evaluation and known failures

See [the complete result](evaluation/baseline.json) and
[evaluation protocol](docs/evaluation.md). Development selection chose hybrid
retrieval with a 0.40 overlap threshold. The final 24-case suite contains 12
answerable and 12 unsupported questions.

| Test measure | Hybrid | BM25 at the same threshold |
| --- | --- | --- |
| Source recall@3 | 1.000 | 1.000 |
| MRR@3 | 1.000 | 1.000 |
| Answerability accuracy | 0.917 | 0.917 |
| Unsupported-question abstention | 0.833 | 0.833 |
| Relevant-source precision among emitted answers | 0.857 | 0.857 |

Hybrid does **not** improve the test results over BM25 here. Two unsupported
requests, about net profit after expenses and June operating expenses, receive
related margin evidence instead of abstention. These failures are retained in
the report. The small author-written corpus and questions are a regression suite,
not independent evidence of enterprise retrieval quality.

Source-ID membership is not entailment. Live LLM answer quality, latency and cost
have **not** been evaluated. The optional model adapter is tested with mocked
responses, including invalid citations and timeouts.

## Optional local generation

Install Ollama and choose/download a model suitable for your machine separately.
Set `OLLAMA_MODEL` to that installed model's name before starting the app. The
default origin is http://127.0.0.1:11434. Select “Local Ollama” in the UI.
Without a working local model the app abstains; it does not silently pretend the
extractive response is an LLM answer.

The adapter calls [Ollama /api/chat](https://docs.ollama.com/api/chat) with a
[JSON schema](https://docs.ollama.com/capabilities/structured-outputs), bounded
context and output, a timeout, and no tools. It accepts only loopback origins.
See [architecture](docs/architecture.md) and [security limits](SECURITY.md).

## Repository guide

- [Finance handbook](docs/finance_handbook.md): fictional definitions and controls.
- [SQL](sql/): transparent revenue, margin, price-gap and quality logic.
- [Data provenance](data/PROVENANCE.json): generation seed, scope and row count.
- [Architecture and API](docs/architecture.md): request path and tradeoffs.
- [Evaluation](docs/evaluation.md): case design, selection and limits.
- [Next experiments](ROADMAP.md): work that remains before stronger claims.

The original starter HTML in Data/ and editor workspace file are retained as
repository history/reference. The application entry point is app.py.
