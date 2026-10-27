def enrich(df):
    df["txn_type"] = df.amount.apply(lambda x: "Credit" if x > 0 else "Debit")

    def category(d):
        d = d.lower()
        if "atm" in d: return "Cash Withdrawal"
        if "upi" in d or "gpay" in d: return "UPI"
        if "emi" in d or "loan" in d: return "Loan/EMI"
        if "salary" in d: return "Income"
        return "Other"

    df["category"] = df.description.apply(category)
    df["counterparty"] = df.description.str.extract(r'([A-Z]{3,})', expand=False)
    return df
