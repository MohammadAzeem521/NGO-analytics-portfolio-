"""
04_ngo_segmentation_clustering.py
----------------------------------------------------------------------
Uses K-Means clustering (scikit-learn) to segment the 10 NGOs into
performance tiers based on their (synthetic) fundraising & engagement
metrics — a lightweight demonstration of applied ML for a portfolio
project. Not intended as a real-world benchmarking tool.
----------------------------------------------------------------------
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

DATA = "../data"
OUT = "./charts"
df = pd.read_csv(f"{DATA}/ngo_features_for_clustering.csv")
df["total_hours"] = df["total_hours"].fillna(0)
df["total_volunteers"] = df["total_volunteers"].fillna(0)

feature_cols = ["total_donations", "avg_donation", "num_donations", "recurring_rate",
                 "total_hours", "total_volunteers"]
X = df[feature_cols].values
X_scaled = StandardScaler().fit_transform(X)

# ---------------- Elbow method to justify k ----------------
inertias = []
K_range = range(1, 7)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
ax.plot(list(K_range), inertias, marker="o", color="#2E5395", linewidth=2)
ax.set_title("Elbow Method — Optimal Number of Clusters")
ax.set_xlabel("Number of Clusters (k)")
ax.set_ylabel("Inertia")
plt.tight_layout()
plt.savefig(f"{OUT}/07_elbow_method.png", bbox_inches="tight")
plt.close()

# ---------------- Fit final model (k=3) ----------------
K_FINAL = 3
kmeans = KMeans(n_clusters=K_FINAL, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# Label clusters by average total_donations (rank-based, human-readable)
cluster_rank = df.groupby("cluster")["total_donations"].mean().sort_values(ascending=False)
label_map = {cluster_rank.index[0]: "High-Performing", cluster_rank.index[1]: "Steady Contributor",
             cluster_rank.index[2]: "Emerging / Growth Potential"}
df["segment"] = df["cluster"].map(label_map)

# ---------------- PCA for 2D visualization ----------------
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(X_scaled)
df["pca_1"], df["pca_2"] = coords[:, 0], coords[:, 1]

fig, ax = plt.subplots(figsize=(9, 7), dpi=150)
palette = {"High-Performing": "#2E5395", "Steady Contributor": "#70AD47",
           "Emerging / Growth Potential": "#ED7D31"}
for seg, color in palette.items():
    sub = df[df["segment"] == seg]
    ax.scatter(sub["pca_1"], sub["pca_2"], label=seg, s=180, color=color, edgecolor="white", linewidth=1.5)
for _, row in df.iterrows():
    ax.annotate(row["ngo_name"].split(" ")[0], (row["pca_1"], row["pca_2"]),
                textcoords="offset points", xytext=(8, 5), fontsize=8.5)
ax.set_title(f"NGO Segmentation (K-Means, k={K_FINAL}) — PCA Projection")
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.legend(loc="best", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUT}/08_ngo_segmentation_clusters.png", bbox_inches="tight")
plt.close()

df[["ngo_name", "segment"] + feature_cols].round(2).to_csv(
    f"{DATA}/ngo_segmentation_results.csv", index=False)

print("Cluster assignment:")
print(df[["ngo_name", "segment"]].to_string(index=False))
print("\nSegmentation complete. Charts + results saved.")
