import pandas as pd

def load_data(filepath):
    df = pd.read_excel(filepath,sheet_name="Year 2010-2011")
    return df

def initial_check(df):
    print("Shape:", df.shape)
    print("\nTypes:\n", df.dtypes)
    print("\nHead:\n", df.head())
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nDescribe:\n", df.describe().T)

def prepare_retail_data(df):
    df = df.copy()

    df.dropna(subset=['Customer ID'],inplace=True)
    df = df[~df["Invoice"].astype(str).str.startswith("C", na=False)]
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]

    df["TotalPrice"] = df["Quantity"] * df["Price"]

    return df

