def map_transaction_to_behavior(row):
    if row.category == "Cash Withdrawal":
        return "High Cash Usage"

    if row.category == "Loan/EMI":
        return "Debt Obligation"

    if row.amount < 0 and abs(row.amount) > 0.8 * abs(row.amount):
        return "Large Outflow"

    if row.amount > 0:
        return "Income Event"

    return "General Spending"
