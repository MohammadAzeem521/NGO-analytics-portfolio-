import sqlite3
import pandas as pd

DB_PATH = "../sql/ngo_analytics.db"
DATA_DIR = "../data"
import os
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE dim_ngo (
    ngo_id TEXT PRIMARY KEY,
    ngo_name TEXT NOT NULL,
    year_founded INTEGER,
    headquarters_city TEXT,
    headquarters_state TEXT,
    organization_type TEXT,
    primary_focus_area TEXT,
    website TEXT
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date TEXT,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER,
    weekday_name TEXT,
    is_weekend INTEGER,
    fiscal_year TEXT
);

CREATE TABLE dim_campaign (
    campaign_id TEXT PRIMARY KEY,
    ngo_id TEXT REFERENCES dim_ngo(ngo_id),
    campaign_name TEXT,
    channel TEXT,
    start_date TEXT,
    end_date TEXT,
    target_amount_inr REAL,
    status TEXT
);

CREATE TABLE fact_donations (
    donation_id TEXT PRIMARY KEY,
    ngo_id TEXT REFERENCES dim_ngo(ngo_id),
    campaign_id TEXT REFERENCES dim_campaign(campaign_id),
    date_id INTEGER REFERENCES dim_date(date_id),
    donor_type TEXT,
    payment_mode TEXT,
    donor_state TEXT,
    is_recurring INTEGER,
    donation_amount_inr REAL
);

CREATE TABLE fact_volunteer_hours (
    log_id TEXT PRIMARY KEY,
    ngo_id TEXT REFERENCES dim_ngo(ngo_id),
    date_id INTEGER REFERENCES dim_date(date_id),
    volunteer_count INTEGER,
    hours_logged INTEGER,
    activity_type TEXT
);

CREATE INDEX idx_fact_donations_ngo ON fact_donations(ngo_id);
CREATE INDEX idx_fact_donations_date ON fact_donations(date_id);
CREATE INDEX idx_fact_donations_campaign ON fact_donations(campaign_id);
CREATE INDEX idx_fact_volunteer_ngo ON fact_volunteer_hours(ngo_id);
CREATE INDEX idx_campaign_ngo ON dim_campaign(ngo_id);
""")
conn.commit()

tables = ["dim_ngo", "dim_date", "dim_campaign", "fact_donations", "fact_volunteer_hours"]
file_map = {
    "dim_ngo": "dim_ngo.csv",
    "dim_date": "dim_date.csv",
    "dim_campaign": "dim_campaign.csv",
    "fact_donations": "fact_donations.csv",
    "fact_volunteer_hours": "fact_volunteer_hours.csv",
}

for t in tables:
    df = pd.read_csv(f"{DATA_DIR}/{file_map[t]}")
    if "is_recurring" in df.columns:
        df["is_recurring"] = df["is_recurring"].astype(int)
    if "is_weekend" in df.columns:
        df["is_weekend"] = df["is_weekend"].astype(int)
    df.to_sql(t, conn, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {t}")

conn.commit()

# Sanity check
cur.execute("SELECT COUNT(*) FROM fact_donations")
print("fact_donations row count:", cur.fetchone()[0])
cur.execute("SELECT SUM(donation_amount_inr) FROM fact_donations")
print("Total donations (INR):", cur.fetchone()[0])

conn.close()
print("SQLite database built successfully:", DB_PATH)
