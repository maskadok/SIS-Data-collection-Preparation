import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED = BASE_DIR / "data" / "cleaned_data.csv"
DB_PATH = BASE_DIR / "data" / "output.db"

def load_data():
    df = pd.read_csv(CLEANED, encoding="utf-8")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS smartphones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating REAL,
            reviews REAL,
            price REAL,
            product_url TEXT UNIQUE,
            category TEXT,
            raw_text TEXT
        );
        """)

        existing = pd.read_sql_query(
            "SELECT product_url FROM smartphones",
            conn
        )

        existing_urls = set(existing["product_url"].tolist())
        df_new = df[~df["product_url"].isin(existing_urls)]

        print(f"Новых записей для вставки: {len(df_new)}")

        df_new.to_sql(
            "smartphones",
            conn,
            if_exists="append",
            index=False
        )

    print("Загрузка завершена.")

if __name__ == "__main__":
    load_data()
