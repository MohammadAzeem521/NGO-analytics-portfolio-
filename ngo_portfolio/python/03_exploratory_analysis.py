"""
03_exploratory_analysis.py
----------------------------------------------------------------------
Exploratory Data Analysis on the NGO donations dataset using pandas,
matplotlib and seaborn. Produces 6 publication-quality charts for the
portfolio README / LinkedIn / Power BI cross-check.
----------------------------------------------------------------------
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})

NAVY = "#1F3864"
DATA = "../data"
OUT = "./charts"

# ---------------- Load ----------------
dim_ngo = pd.read_csv(f"{DATA}/dim_ngo.csv")
dim_date = pd.read_csv(f"{DATA}/dim_date.csv", parse_dates=["date"])
dim_campaign = pd.read_csv(f"{DATA}/dim_campaign.csv")
fact_donations = pd.read_csv(f"{DATA}/fact_donations.csv")
fact_volunteer = pd.read_csv(f"{DATA}/fact_volunteer_hours.csv")

# ---------------- Data cleaning checks ----------------
print("Missing values check:")
print(fact_donations.isnull().sum())
print("\nDuplicate donation_id count:", fact_donations["donation_id"].duplicated().sum())
print("Negative/zero donation amounts:", (fact_donations["donation_amount_inr"] <= 0).sum())

# ---------------- Merge for analysis ----------------
df = fact_donations.merge(dim_ngo, on="ngo_id").merge(dim_date, on="date_id")

# ============================================================
# CHART 1: Total donations by NGO (bar)
# ============================================================
ngo_totals = df.groupby("ngo_name")["donation_amount_inr"].sum().sort_values()
fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
ngo_totals.plot(kind="barh", ax=ax, color=sns.color_palette("Blues_d", len(ngo_totals)))
ax.set_title("Total Simulated Donations by NGO (2021-2025)")
ax.set_xlabel("Total Donations (INR)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"₹{x/1e6:.1f}M"))
plt.tight_layout()
plt.savefig(f"{OUT}/01_total_donations_by_ngo.png", bbox_inches="tight")
plt.close()

# ============================================================
# CHART 2: Monthly donation trend (line)
# ============================================================
monthly = df.groupby(df["date"].dt.to_period("M"))["donation_amount_inr"].sum()
fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
monthly.plot(ax=ax, color=NAVY, linewidth=1.8)
ax.set_title("Monthly Donation Trend (All NGOs Combined)")
ax.set_ylabel("Total Donations (INR)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"₹{x/1e6:.1f}M"))
plt.tight_layout()
plt.savefig(f"{OUT}/02_monthly_donation_trend.png", bbox_inches="tight")
plt.close()

# ============================================================
# CHART 3: Donor type distribution (pie)
# ============================================================
donor_mix = df.groupby("donor_type")["donation_amount_inr"].sum()
fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
ax.pie(donor_mix, labels=donor_mix.index, autopct="%1.1f%%", startangle=90,
       colors=sns.color_palette("Set2"), wedgeprops=dict(edgecolor="white"))
ax.set_title("Donation Value Share by Donor Type")
plt.tight_layout()
plt.savefig(f"{OUT}/03_donor_type_mix.png", bbox_inches="tight")
plt.close()

# ============================================================
# CHART 4: Donation amount distribution by donor type (boxplot)
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
sns.boxplot(data=df, x="donor_type", y="donation_amount_inr", ax=ax, palette="Blues")
ax.set_yscale("log")
ax.set_title("Donation Amount Distribution by Donor Type (log scale)")
ax.set_ylabel("Donation Amount (INR, log scale)")
plt.tight_layout()
plt.savefig(f"{OUT}/04_donation_distribution_boxplot.png", bbox_inches="tight")
plt.close()

# ============================================================
# CHART 5: Correlation heatmap (NGO-level aggregated features)
# ============================================================
ngo_features = df.groupby("ngo_name").agg(
    total_donations=("donation_amount_inr", "sum"),
    avg_donation=("donation_amount_inr", "mean"),
    num_donations=("donation_id", "count"),
    recurring_rate=("is_recurring", "mean"),
).reset_index()
vol_features = fact_volunteer.merge(dim_ngo, on="ngo_id").groupby("ngo_name").agg(
    total_hours=("hours_logged", "sum"),
    total_volunteers=("volunteer_count", "sum"),
).reset_index()
ngo_features = ngo_features.merge(vol_features, on="ngo_name", how="left")

fig, ax = plt.subplots(figsize=(7.5, 6), dpi=150)
corr = ngo_features.drop(columns="ngo_name").corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, square=True)
ax.set_title("Correlation Matrix — NGO-Level Metrics")
plt.tight_layout()
plt.savefig(f"{OUT}/05_correlation_heatmap.png", bbox_inches="tight")
plt.close()

# ============================================================
# CHART 6: Top donor states (bar)
# ============================================================
state_totals = df.groupby("donor_state")["donation_amount_inr"].sum().sort_values(ascending=False).head(8)
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
state_totals.plot(kind="bar", ax=ax, color=sns.color_palette("Oranges_d", len(state_totals)))
ax.set_title("Top 8 Donor States by Total Contribution")
ax.set_ylabel("Total Donations (INR)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"₹{x/1e6:.1f}M"))
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(f"{OUT}/06_top_donor_states.png", bbox_inches="tight")
plt.close()

# Save NGO-level feature table for the ML step
ngo_features.to_csv(f"{DATA}/ngo_features_for_clustering.csv", index=False)

print("\nEDA complete. 6 charts saved to", OUT)
print(ngo_features.round(2))
