# 🤖 Buy-and-Wait — Autonomous AI Financial Decision & Budget Advisory Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/HackerRank-Orchestrate_Hackathon-2EC866?style=for-the-badge&logo=hackerrank&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Architecture-REST_Microservice-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Decision_Engine-Multi--Stream_Risk-orange?style=for-the-badge" />
</p>

> **Buy-and-Wait** is an autonomous AI financial decision agent engineered during the 24-hour **HackerRank Orchestrate Hackathon (September 2026)**. It evaluates whether a user can safely afford a discretionary expense by analyzing multi-stream financial records, recurring liabilities, currency rates, installment scheduling, and cashflow risk.

---

## 🏆 Hackathon Recognition
* **Event**: HackerRank Orchestrate (Sept 2026) — 24-Hour International Challenge
* **Outcome**: Official **Certificate of Achievement** for building and deploying an end-to-end autonomous decision pipeline.
* **Test Evaluation**: Evaluated across **250+ financial evaluation test cases** across 7 multi-modal tabular datasets with zero unhandled exceptions.

---

## 💡 The Core Problem
When a user asks: **"Can I afford to buy this item right now?"**, traditional banking apps only check the current account balance. 

**Buy-and-Wait** solves the hidden pitfalls:
1. **Pending Commitments**: Upcoming rent, EMI installments, utility bills, and insurance.
2. **Dynamic Cashflow Forecasting**: Projected salary credits vs. mandatory spending over a 30–90 day horizon.
3. **Safety Buffer**: Ensures the user never drops below their preferred emergency minimum balance.
4. **Actionable Recommendations**: Recommends `FULL_PAYMENT`, `INSTALLMENTS` (with custom tenure), `WAIT / DEFER`, or `DECLINE`.

---

## 🛠️ Architecture & Tech Stack

```
User Purchase Request ──► [ Input Sanitization & Normalization ]
                                   │
                                   ▼
[ Multi-Source Datasets ] ──► [ Financial Forecasting Engine ]
  • Cash Balances                  │
  • Recurring Liabilities          ▼
  • Installment Rules     ──► [ Heuristic Risk & Solvency Engine ]
  • Currency Rates                 │
                                   ▼
                         [ Recommendation Agent ]
                         • Decision: FULL / INSTALLMENT / WAIT
                         • Risk Score & Cashflow Runway
                         • Explanatory Reasoning Report
```

* **Core Engine**: Python 3.11, Pandas, NumPy
* **Backend & API**: Flask / Python REST Service, SQLite (ACID-compliant storage)
* **Frontend / UI**: Web Dashboard (HTML5, CSS3, Jinja2) + React Native Mobile App (`BuyOrWaitApp`)
* **Decision Logic**: Heuristic cashflow projection, conflict resolution matrix, installment amortizer

---

## ✨ Key Features
* **Multi-Dataset Synthesis**: Concurrently processes 7 CSV streams (balances, transactions, recurring bills, exchange rates, merchant catalogues).
* **Smart Conflict Resolution**: Resolves overlapping liabilities, duplicate requests, and date mismatches automatically.
* **Installment Feasibility Matrix**: Calculates interest-free vs. EMI cost impacts over time to safeguard emergency liquid reserves.
* **Audit & Logging**: Detailed step-by-step reasoning logs explaining why an expense was approved, deferred, or rejected.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/kaushallakshya71-a11y/Buy-and-Wait.git
cd Buy-and-Wait
```

### 2. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r code/requirements.txt  # or pip install pandas flask
```

### 3. Run the decision agent & server
```bash
python3 server.py
# Open http://localhost:5000 in your browser
```

---

## 👤 Author
**Lakshya Kaushal**  
* B.Tech Computer Science & Engineering (AI & ML) — MIPS, Kanpur  
* [LinkedIn](https://linkedin.com/in/lakshya-kaushal) • [GitHub](https://github.com/kaushallakshya71-a11y) • [Portfolio](https://portfolio-1-ewg2.onrender.com)
