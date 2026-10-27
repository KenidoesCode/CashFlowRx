import pandas as pd
import numpy as np

def risk_scores(df):
    metrics = {}

    df["date"] = pd.to_datetime(df.date)

    income = df[df.amount > 0]
    debit = df[df.amount < 0]

    monthly_income = income.groupby(df.date.dt.to_period("M")).amount.sum()

    mean = monthly_income.mean() or 1
    std = monthly_income.std() or 0

    income_volatility = std / mean
    metrics["income_risk"] = (
        10 if income_volatility < 0.2 else
        30 if income_volatility < 0.4 else
        60 if income_volatility < 0.6 else
        85
    )

    ratio = abs(debit.amount.sum()) / mean
    metrics["spending_risk"] = (
        10 if ratio < 0.6 else
        30 if ratio < 0.8 else
        60 if ratio < 1.0 else
        90
    )

    net = income.amount.sum() - abs(debit.amount.sum())
    metrics["liquidity_risk"] = 10 if net > 0 else 80

    emi = df[df.category == "Loan/EMI"].amount.abs().sum()
    metrics["debt_risk"] = (
        10 if emi/mean < 0.2 else
        40 if emi/mean < 0.35 else
        70 if emi/mean < 0.5 else
        90
    )

    cash_ratio = len(df[df.category == "Cash Withdrawal"]) / len(df)
    metrics["cash_risk"] = (
        10 if cash_ratio < 0.05 else
        40 if cash_ratio < 0.15 else
        80
    )

    final = (
        0.25 * metrics["income_risk"] +
        0.25 * metrics["spending_risk"] +
        0.20 * metrics["liquidity_risk"] +
        0.20 * metrics["debt_risk"] +
        0.10 * metrics["cash_risk"]
    )

    metrics["final_score"] = round(final, 1)
    return metrics
