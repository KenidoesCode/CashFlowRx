import pandas as pd

def cashflow(df):
    df["date"] = pd.to_datetime(df.date)
    daily = df.groupby("date").amount.sum()
    return daily
