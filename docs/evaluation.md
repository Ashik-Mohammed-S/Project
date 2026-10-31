# Evaluation protocol

The 48 cases are author-written examples over a 13-document corpus (12 handbook
notes plus one derived SQL snapshot). Split membership is committed in
data/eval_cases.json: 24 development cases and 24 test cases. Questions are distinct
across splits. The benchmark was authored together with this prototype; it is not
an external blind test and should not be presented as one.

Development cases select BM25 versus BM25/trigram rank fusion and one of four
confidence thresholds. Selection maximizes correct relevant-source answer or
correct abstention, with MRR as a tie-breaker. Configuration is written to
config.json. The fixed test suite is then evaluated once for the reported version.

Initial draft questions had overly easy off-topic negatives. Before freezing the
release suite, additional unsupported in-domain requests were added to both splits
to expose abstention failures. The release evaluation retains the two observed
test failures rather than adjusting rules against those test questions.

Metrics:

- Source recall@3: fraction of annotated relevant source IDs in the first three
  results, averaged over answerable cases.
- MRR@3: reciprocal first relevant-source rank, zero when absent.
- Answerability accuracy: whether the system answers an answerable case or abstains
  on an unsupported one. This does not require the selected answer source to match.
- Relevant-source precision: emitted answers with an annotated relevant citation,
  divided by all emitted answers. It is not semantic factuality.
- Unsupported abstention: fraction of unsupported questions with no answer.

All results and per-question failures are in evaluation/baseline.json, together
with SHA-256 hashes of UTF-8 source text normalized to LF newlines. `evaluate.py --check` regenerates selection and
metrics and compares them exactly to the committed baseline. Corpus or evaluation
changes require an inspected baseline refresh, not an automatic success threshold
reduction.

CI does not call a language model. Ollama API response parsing, citation membership,
timeouts and remote-origin rejection are tested with mocked transports. No live
generation accuracy, faithfulness, token usage, cost or model-vs-model result is
claimed. Larger independently labeled corpora and a live-model evaluation are next.
