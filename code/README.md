# Buy or Wait? — Financial Decision Agent

HackerRank Orchestrate (September 2026) Challenge Submission.

## 1. Overview

This system is an autonomous financial decision agent that evaluates purchase and payment requests against a user's reconstructed financial profile. For each evaluation request in `dataset/requests.csv`, the agent produces a grounded recommendation complying with all financial safety constraints, minimum balance requirements, and preference rules.

### Key Capabilities:
- **Cash Flow Simulation**: Day-by-day 90-day cash flow simulation strictly enforcing `minimum_balance_to_keep`.
- **Payment Method Hierarchy**: Evaluates `full_payment`, `installments`, `partial_payment`, `wait`, and flexible spending changes (`stop:<event_id>`, `reduce_to:<event_id>:<amt>`).
- **Section 189 Tie-Breaker Logic**: Prioritizes plans completing on or before `desired_completion_date`, avoiding spending changes, minimizing total payment amount, starting earlier, and requiring fewer payments.
- **Multimodal & Supporting Evidence Integration**: Accurately resolves dated exchange rates, seller payment terms, verified receipt/bill OCR amounts (`dataset/media/images/`), and message updates (salary adjustments, rent modifications).
- **Deterministic & High Performance**: Runs in seconds with zero external API dependencies or token costs, guaranteeing 100% reproducibility.

---

## 2. Directory Structure

```text
code/
├── main.py                     # Primary entry point: evaluates dataset/requests.csv and writes output.csv
├── data_loader.py              # CSV ingestion, dated FX lookup, image resolution, and message parsing
├── extractor.py                # OCR parser and regex extractors for messages and media
├── finance_engine.py           # 90-day daily cash-flow forecasting and commitment calculator
├── payment_planner.py          # Candidate payment plan builder and Section 189 optimizer
├── decision_engine.py          # Recommendation synthesis, formatting, and explanation generation
├── evaluator.py                # Validation benchmark against sample_requests.csv
├── evaluation/
│   └── usage_report.md         # Final model calls, token usage, and cost summary
└── README.md                   # This documentation
```

---

## 3. Setup and Execution

### Requirements
- Python 3.9+
- Standard packages: `pandas`, `numpy`

### Installation
```bash
pip install pandas numpy
```

### Running the Solution
From the repository root:
```bash
python3 code/main.py
```

This will:
1. Ingest all datasets from `dataset/`.
2. Evaluate all 250 evaluation requests in `dataset/requests.csv`.
3. Generate the required root-level `output.csv`.
4. Generate `code/evaluation/usage_report.md`.

### Running Evaluation Against Public Samples
To evaluate performance against ground-truth sample requests:
```bash
python3 code/evaluator.py
```
