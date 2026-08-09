import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

color = ["lightblue", "darkblue"]

fig = plt.figure(figsize=(12, 12), constrained_layout=True)
gs = fig.add_gridspec(2, 2)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])

# A= curated
curated = pd.read_csv("curated_interactors.tsv", sep="\t")
curated = curated.sort_values("iPTM", ascending=False)

x = np.arange(len(curated))
width = 0.35
ax1.bar(x - width/2, curated["iPTM"], width, label="ipTM", color="lightgreen")
ax1.bar(x + width/2, curated["actifPTM"], width, label="actifpTM", color="darkgreen")
ax1.set_xticks(x)
ax1.set_xticklabels(curated["Complex"], rotation=45, ha="right")
ax1.set_ylabel("Score")
ax1.legend()

# wgcna
wgcna = pd.read_csv("af3_wgcna_output/wgcna_scored.tsv", sep="\t")
wgcna = wgcna.dropna(subset=["actifptm"])
sns.boxplot(data=wgcna, x="Tag", y="actifptm",
            order=["wgcna_top10", "genome_random"], ax=ax2, hue="Tag",
            palette=color, legend=False)
ax2.set_xlabel("Gene selection")
ax2.set_xticklabels(["Top WGCNA coexpressed", "Random gene"])
ax2.set_ylabel("actifptm")


# mapx
mapx = pd.read_csv("af3_mapx_output/mapx_scored.tsv", sep="\t")
mapx = mapx.dropna(subset=["actifptm"])
sns.boxplot(data=mapx, x="Tag", y="actifptm",
            order=["passed", "not_passed"], ax=ax3, hue="Tag",
            palette=color, legend=False)
ax3.set_xlabel("MAPX prediction")
ax3.set_xticklabels(["Top Predicted MAP-X Interactors", "Below Threshold Interactor"])
ax3.set_ylabel("actifptm")

for ax, label in zip([ax1, ax2, ax3], ["A", "B", "C"]):
    ax.text(-0.05, 1.05, label, transform=ax.transAxes,
            fontsize=16, fontweight="bold", va="bottom", ha="right")


plt.savefig("af3_panel.png", dpi=300)
plt.show()
