import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW = BASE_DIR / "data" / "row_data.csv"
CLEANED = BASE_DIR / "data" / "cleaned_data.csv"

def clean_data():
    df = pd.read_csv(RAW, encoding="utf-8")

    df.drop_duplicates(subset=["product_url"], inplace=True)

    df["name"] = df["name"].fillna("Unknown")
    df["price"] = df["price"].fillna(0)
    df["rating"] = df["rating"].fillna(0.0)
    df["reviews"] = df["reviews"].fillna(0)

    df["name"] = df["name"].str.strip().str[9:]
    df["raw_text"] = df["raw_text"].astype(str).str.strip()

    df["price"] = df["price"].astype(int)
    df["rating"] = df["rating"].astype(float)
    df["reviews"] = df["reviews"].astype(int)

    df.to_csv(CLEANED, index=False, encoding="utf-8")
    print(f"Cleaned dataset saved: {CLEANED}, rows: {len(df)}")

if __name__ == "__main__":
    clean_data()
