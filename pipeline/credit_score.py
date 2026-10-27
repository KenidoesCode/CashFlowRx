def estimate_credit_score(df):
    score = 900
    debit = abs(df[df.amount < 0].amount.sum())
    credit = df[df.amount > 0].amount.sum()

    ratio = debit / max(credit, 1)
    if ratio > 0.9: score -= 120
    elif ratio > 0.7: score -= 60

    score -= min(len(df[df.category == "Cash Withdrawal"]) * 8, 80)
    score -= min(len(df[df.category == "Loan/EMI"]) * 15, 150)

    return max(300, min(900, score))
