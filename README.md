# RISK# 🏦 Bank Statement Risk Analyzer

An explainable, deterministic financial risk analysis tool that evaluates bank statements and generates a professional risk report with visual relationship graphs.

  Features
 PDF bank statement ingestion
- Transaction categorization & risk tagging
- Explainable risk scoring (no black-box AI)
- Obsidian-style relationship graph:
  Transactions → Behaviors → Risk Dimensions → Final Risk
- Cashflow volatility analysis
- Professional PDF risk report generation

## 🧠 Risk Methodology
Risk is calculated across five dimensions:
- Income Stability
- Spending Discipline
- Liquidity Health
- Debt Load
- Cash Dependency

Each dimension contributes to a weighted final risk score.

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
