# Next experiments toward applied-AI roles

Completed: synthetic finance ledger; metric definitions; allowlisted SQL; BM25
baseline; trigram retrieval comparison; reproducible dev/test protocol; evidence
answers; abstention; optional local-model adapter; Flask API and CI.

1. Independently label a larger corpus and lock a new test set. Include adjacent
   unsupported finance requests, conflicting definitions and outdated policies.
2. Evaluate an installed local LLM against the extractive baseline, measuring
   answer correctness, support for each claim, citation completeness, abstention,
   p50/p95 latency and token counts. Report model/version and hardware.
3. Compare embeddings and a reranker only after establishing the stronger corpus
   baseline. Retain results where added complexity fails to help.
4. Improve the two observed unsupported-expense failures using development-only
   work and validate on new unseen questions, rather than patching test phrases.
5. Add document version/effective-date handling, authenticated multi-user access,
   per-source authorization and scoped read-only data connectors.
6. Add container packaging, deployment traces, concurrency/load tests and budgets
   before describing this as a production service.

This roadmap is preparation for a 2027 job search, not a prediction that any
particular tool or architecture will be required in 2027. Completed work and
planned work remain separately labeled.
