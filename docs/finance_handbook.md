# Fictional retail finance handbook

Author-written sample evidence for an independent portfolio project. These are not employer policies.

## Scope

Harbor Retail is a fictional retailer. The data is generated with seed 2027 and contains no Walgreens, TCS, customer, patient, prescription or internal contract information. This independent portfolio project is not a Walgreens system and has no employer endorsement. It supports retail finance evidence discovery and read-only analysis, not clinical or financial advice.

## Net revenue

Net revenue is units multiplied by unit selling price minus the line discount. Money is stored as integer cents. Taxes, rebates and returns are outside this synthetic ledger's scope. Net revenue is not the same as cash collected. The monthly_margin SQL report aggregates net revenue by month.

## Gross margin

Gross margin amount equals net revenue minus units multiplied by unit cost. Gross margin rate is total gross margin divided by total net revenue. Aggregate the numerator and denominator before division; do not average row-level percentages. Zero revenue produces a null rate. Gross margin is not net profit because operating expenses are excluded.

## Contract exceptions

A price-floor exception occurs when actual unit price is below the contract floor. Potential price gap equals units multiplied by contract floor minus actual unit price, only on below-floor lines. This excludes discounts. A flagged gap is a review candidate, not evidence of recoverable or realized savings. Contract amendments and effective dates require human verification before action.

## Data quality

Each ledger line must have a unique line ID, positive units, nonnegative prices and costs, and a nonnegative discount no greater than gross sales. Duplicate IDs are rejected at load by a primary key. A price below the contract floor is a business exception rather than a malformed record. Data quality failures should block reliance on the financial reports.

## Reconciliation

The ledger grain is one product, store and month sales line. Reconcile monthly net revenue and cost totals to source extracts before publishing dashboards. Aggregate facts before joining one-to-many contract history, or duplicate matches can inflate revenue. Document dimensions, effective dates and exclusions in a metric contract.

## Read-only analytics

Only three committed SQL reports are callable: monthly_margin, contract_leakage and data_quality. User questions and generated text are never executed as SQL. The SQLite connection is switched to query-only after loading. The application cannot update contracts, approve pricing, email stakeholders or connect to employer databases.

## Local generation

The default answer mode quotes retrieved evidence without an LLM. Optional local generation calls an explicitly configured Ollama model on localhost. Every non-abstaining generated answer must return at least one retrieved source ID and no unknown source IDs. Citation membership checks do not prove semantic entailment or prevent all hallucinations. Live LLM quality has not been evaluated in the initial release.

## Abstention

The assistant abstains when retrieval confidence is below a threshold selected on development cases. Questions requesting private employer data, patient details, secrets or policy overrides are blocked by illustrative rules. These pattern checks are limited regression defenses, not a complete prompt-injection security system. Live stock prices and employer financial results are not in this corpus.

## Evaluation

Development cases select retrieval configuration and the abstention threshold. Separate test cases report source recall at three, mean reciprocal rank, answerability accuracy and abstention behavior. The authored corpus is small and synthetic. Citation validity is a structural measure, not a factuality score. Test results do not establish enterprise-scale or production LLM performance.

## Forecasting

The current finance copilot does not train a forecasting model. A future forecasting experiment must use chronological holdouts and compare with seasonal or last-value baselines. Random train-test splitting can leak temporal information. Do not claim historical revenue reporting is a forward forecast or a causal estimate of pricing impact.

## Operations

The service has a health endpoint and CI tests for ledger reconciliation, report access controls, retrieval, abstention and local-model output contracts. Responses include mode, source IDs, request ID and elapsed milliseconds. Logs avoid raw questions and evidence text. There is no production deployment or authenticated enterprise data connection in the initial release.

