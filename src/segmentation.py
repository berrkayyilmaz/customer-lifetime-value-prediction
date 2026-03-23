import pandas as pd

def create_cltv_segments(df):
    df = df.copy()
    df["segment"] = pd.qcut(df["clv"], 4, labels=["D","C","B","A"])
    return df

def segment_summary(df):
    summary = df.groupby("segment").agg(
        customer_count=("Customer ID", "count"),
        avg_clv=("clv", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary","mean")
    ).reset_index()

    return summary