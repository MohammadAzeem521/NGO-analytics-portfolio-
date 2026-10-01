"""
generate_synthetic_data.py
----------------------------------------------------------------------
Generates a SIMULATED donations / campaigns / volunteer dataset layered
on top of the 10 real, research-verified NGOs (see ngo_data.py).

IMPORTANT DISCLOSURE:
The NGO profile fields (name, founder, mission, HQ, year founded, etc.)
are REAL and sourced from official websites (see ngo_data.py / main
research report). The donation amounts, donor records, campaign
performance and volunteer hours below are SYNTHETIC / RANDOMLY
GENERATED for the sole purpose of building a realistic SQL + Power BI
+ Python analytics portfolio project. They do NOT represent actual
financial data of these organisations.
----------------------------------------------------------------------
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from ngo_data import NGOS

random.seed(42)
np.random.seed(42)

# ------------------------------------------------------------------
# 1. DIM_NGO  (real, verified research data -> flattened for the model)
# ------------------------------------------------------------------
dim_ngo = pd.DataFrame([{
    "ngo_id": f"NGO{n['sn']:02d}",
    "ngo_name": n["name"],
    "year_founded": n["year_founded"],
    "headquarters_city": n["hq"],
    "headquarters_state": n["state"].split(" / ")[0],
    "organization_type": n["org_type"].split(" (")[0],
    "primary_focus_area": n["area_of_work"].split(",")[0].strip(),
    "website": n["website"],
} for n in NGOS])

# ------------------------------------------------------------------
# 2. DIM_DATE  (5-year window: 2021-2025, daily grain)
# ------------------------------------------------------------------
date_range = pd.date_range("2021-01-01", "2025-12-31", freq="D")
dim_date = pd.DataFrame({"date": date_range})
dim_date["date_id"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["date"].dt.year
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
dim_date["day"] = dim_date["date"].dt.day
dim_date["weekday_name"] = dim_date["date"].dt.strftime("%A")
dim_date["is_weekend"] = dim_date["date"].dt.weekday >= 5
fy_end_year = pd.Series(np.where(dim_date["month"] >= 4, dim_date["year"] + 1, dim_date["year"]))
dim_date["fiscal_year"] = np.where(dim_date["month"] >= 4, dim_date["year"], dim_date["year"] - 1).astype(str) + "-" + \
                           (fy_end_year % 100).astype(str).str.zfill(2)
dim_date = dim_date[["date_id", "date", "year", "quarter", "month", "month_name", "day",
                      "weekday_name", "is_weekend", "fiscal_year"]]

# ------------------------------------------------------------------
# 3. DIM_CAMPAIGN  (5-8 campaigns per NGO)
# ------------------------------------------------------------------
CAMPAIGN_THEMES = ["Education Drive", "Emergency Relief", "Health Camp", "Nutrition Program",
                    "Skill Development", "Winter Clothing Drive", "Disaster Response",
                    "Women Empowerment Fund", "Clean Water Initiative", "Digital Literacy Push",
                    "Elderly Care Support", "Wildlife Protection Fund", "Girl Child Education"]
CHANNELS = ["Online Portal", "Corporate CSR", "Peer-to-Peer", "Offline Event", "Social Media"]
STATUSES = ["Completed", "Completed", "Completed", "Ongoing"]

campaign_rows = []
campaign_id_counter = 1
for _, ngo in dim_ngo.iterrows():
    n_campaigns = random.randint(5, 8)
    for _ in range(n_campaigns):
        start = pd.Timestamp("2021-01-01") + timedelta(days=random.randint(0, 1700))
        duration = random.randint(20, 120)
        end = start + timedelta(days=duration)
        target = random.choice([250000, 500000, 750000, 1000000, 1500000, 2000000, 3000000, 5000000])
        campaign_rows.append({
            "campaign_id": f"CMP{campaign_id_counter:04d}",
            "ngo_id": ngo["ngo_id"],
            "campaign_name": f"{ngo['ngo_name'].split(' ')[0]} {random.choice(CAMPAIGN_THEMES)} {start.year}",
            "channel": random.choice(CHANNELS),
            "start_date": start.date(),
            "end_date": end.date(),
            "target_amount_inr": target,
            "status": random.choice(STATUSES),
        })
        campaign_id_counter += 1
dim_campaign = pd.DataFrame(campaign_rows)

# ------------------------------------------------------------------
# 4. FACT_DONATIONS  (~6,000 synthetic donation transactions)
# ------------------------------------------------------------------
DONOR_TYPES = ["Individual", "Corporate", "Foundation", "Government Grant"]
DONOR_TYPE_WEIGHTS = [0.62, 0.22, 0.11, 0.05]
PAYMENT_MODES = ["UPI", "Credit Card", "Net Banking", "Cheque", "NEFT/RTGS"]
INDIAN_STATES = ["Delhi", "Maharashtra", "Karnataka", "Gujarat", "Tamil Nadu", "Uttar Pradesh",
                  "West Bengal", "Telangana", "Rajasthan", "Punjab", "Kerala", "Haryana"]

N_DONATIONS = 6000
fact_rows = []
ngo_ids = dim_ngo["ngo_id"].tolist()
# Give some NGOs more donation volume than others (realistic skew)
ngo_weights = np.random.dirichlet(np.ones(len(ngo_ids)) * 1.5)

for i in range(1, N_DONATIONS + 1):
    ngo_id = np.random.choice(ngo_ids, p=ngo_weights)
    ngo_campaigns = dim_campaign[dim_campaign["ngo_id"] == ngo_id]
    campaign = ngo_campaigns.sample(1).iloc[0]
    donation_date = pd.Timestamp(campaign["start_date"]) + timedelta(
        days=random.randint(0, max(1, (pd.Timestamp(campaign["end_date"]) - pd.Timestamp(campaign["start_date"])).days)))
    donor_type = np.random.choice(DONOR_TYPES, p=DONOR_TYPE_WEIGHTS)
    if donor_type == "Individual":
        amount = round(np.random.lognormal(mean=7.2, sigma=0.9), -1)
        amount = min(amount, 50000)
    elif donor_type == "Corporate":
        amount = round(np.random.lognormal(mean=10.5, sigma=1.0), -2)
        amount = min(amount, 2000000)
    elif donor_type == "Foundation":
        amount = round(np.random.lognormal(mean=10.0, sigma=0.8), -2)
        amount = min(amount, 1500000)
    else:
        amount = round(np.random.lognormal(mean=11.0, sigma=0.6), -3)
        amount = min(amount, 3000000)
    amount = max(amount, 100)

    fact_rows.append({
        "donation_id": f"DN{i:06d}",
        "ngo_id": ngo_id,
        "campaign_id": campaign["campaign_id"],
        "date_id": int(donation_date.strftime("%Y%m%d")),
        "donor_type": donor_type,
        "payment_mode": random.choice(PAYMENT_MODES),
        "donor_state": random.choice(INDIAN_STATES),
        "is_recurring": random.random() < 0.28,
        "donation_amount_inr": round(float(amount), 2),
    })

fact_donations = pd.DataFrame(fact_rows)

# ------------------------------------------------------------------
# 5. FACT_VOLUNTEER_HOURS (~1,500 synthetic volunteer log entries)
# ------------------------------------------------------------------
N_VOLUNTEER = 1500
vol_rows = []
for i in range(1, N_VOLUNTEER + 1):
    ngo_id = np.random.choice(ngo_ids, p=ngo_weights)
    log_date = pd.Timestamp("2021-01-01") + timedelta(days=random.randint(0, 1825))
    vol_rows.append({
        "log_id": f"VOL{i:05d}",
        "ngo_id": ngo_id,
        "date_id": int(log_date.strftime("%Y%m%d")),
        "volunteer_count": random.randint(2, 45),
        "hours_logged": random.randint(10, 400),
        "activity_type": random.choice(["Fundraising Event", "Field Distribution", "Teaching/Training",
                                          "Health Camp Support", "Awareness Drive", "Admin Support"]),
    })
fact_volunteer = pd.DataFrame(vol_rows)

# ------------------------------------------------------------------
# SAVE EVERYTHING
# ------------------------------------------------------------------
OUT = "../data"
dim_ngo.to_csv(f"{OUT}/dim_ngo.csv", index=False)
dim_date.to_csv(f"{OUT}/dim_date.csv", index=False)
dim_campaign.to_csv(f"{OUT}/dim_campaign.csv", index=False)
fact_donations.to_csv(f"{OUT}/fact_donations.csv", index=False)
fact_volunteer.to_csv(f"{OUT}/fact_volunteer_hours.csv", index=False)

print("dim_ngo:", dim_ngo.shape)
print("dim_date:", dim_date.shape)
print("dim_campaign:", dim_campaign.shape)
print("fact_donations:", fact_donations.shape)
print("fact_volunteer:", fact_volunteer.shape)
print("Total simulated donation value (INR):", round(fact_donations['donation_amount_inr'].sum(), 2))
print("Data generation complete.")
