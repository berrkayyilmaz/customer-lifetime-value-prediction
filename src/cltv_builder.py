import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter

def create_cltv_df(df, country="United Kingdom"):
    df = df.copy()
    df = df[df["Country"] == country]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=2)

    cltv_df = df.groupby("Customer ID").agg(
        {
            "InvoiceDate": [
                lambda x: (x.max() - x.min()).days,
                lambda x: (analysis_date - x.min()).days
            ],
            "Invoice": lambda x: x.nunique(),
            "TotalPrice": lambda x: x.sum()
        }
    )

    cltv_df.columns = ["recency","T","frequency","monetary"]
    cltv_df = cltv_df.reset_index()

    cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]

    cltv_df = cltv_df[(cltv_df["frequency"] > 1)]
    cltv_df = cltv_df[cltv_df["monetary"] > 0]

    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    return cltv_df

def fit_bgf(cltv_df):
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df["frequency"], cltv_df["recency"],cltv_df["T"])
    return bgf

def fit_ggf(cltv_df):
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df["frequency"], cltv_df["monetary"])
    return ggf

def calculate_cltv(cltv_df, bgf, ggf, month=6):
    cltv = ggf.customer_lifetime_value(
        bgf,
        cltv_df["frequency"],
        cltv_df["recency"],
        cltv_df["T"],
        cltv_df["monetary"],
        time=month,
        freq="W",
        discount_rate=0.01
    )

    result = cltv_df.copy()
    result["clv"] = cltv.values
    return result