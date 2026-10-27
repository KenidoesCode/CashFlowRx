def tag_risks(df):
    """
    Tag individual transactions with a basic risk label.
    This is for manual review & reporting.
    """

    df = df.copy()
    df["risk_tag"] = "Low"

    # High-risk patterns
    df.loc[df.category == "Loan/EMI", "risk_tag"] = "High"
    df.loc[df.category == "Cash Withdrawal", "risk_tag"] = "Medium"

    # Large debits are riskier
    high_debit_threshold = abs(df.amount).quantile(0.90)

    df.loc[
        (df.amount < 0) & (abs(df.amount) >= high_debit_threshold),
        "risk_tag"
    ] = "High"

    return df


def overall_risk(metrics, credit_score):
    """
    Account-level risk classification.
    """

    if credit_score < 550:
        return "High Risk"

    if metrics["net_cashflow"] < 0:
        return "Medium–High Risk"

    if metrics["cash_withdrawals"] > 10:
        return "Medium Risk"

    return "Low Risk"
