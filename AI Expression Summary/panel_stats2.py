# a script to plot the stats analysis, panel A= score difference bar chart per gene, B= observation counts and C= preffered detail
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

plt.rcParams.update({"font.size": 14})

### got claude to fix some of the study name discrepancies across genes
_manual = {
    "Gametocyte Transcriptomes (Lasonder et al)":
        "Gametocyte Transcriptomes (Lasonder et al.)",
    "Transcriptome of sequestration phenotypes (Kamaliddin et al)":
        "Transcriptome of sequestration phenotypes (Kamaliddin et al.)",
    "Mosquito or cultured sporozoites and blood stage transcriptome (NF54)":
        "Mosquito or cultured sporozoites and blood stage transcriptome (NF54) (Hoffmann et al.)",
    "Polysomal and steady-state asexual stage transcriptomes":
        "Polysomal and steady-state asexual stage transcriptomes (Bunnik et al.)",
    "Strand specific transcriptomes of 4 life cycle stages":
        "Strand specific transcriptomes of 4 life cycle stages (Lopez-Barragan et al.)",
}

def normalize_study(s):
    s = s.strip()
    s = re.sub(r'<[^>]+>', '', s)              # remove HTML tags e.g. <i>...</i>
    s = re.sub(r'\s*\|.*$', '', s)             # remove | BI: 5 annotations
    s = s.replace("*", "")
    s = re.sub(r'\s*\(RNA-?seq\)?\s*$', '', s) # remove trailing (RNA-seq) or (RNA-seq
    deficit = s.count('(') - s.count(')')
    if deficit > 0:
        s += ')' * deficit                     # close any unclosed parentheses
    s = s.strip()
    return _manual.get(s, s)



#### script

#get the data for each sheet (one sheet is one gene)
sheets = pd.read_excel("stage_specifc/scores_excel_genes.xlsx", sheet_name=None)
data = {}
for gene, df in sheets.items():
    df.columns = ["Study", "Percentile", "Score", "Difference"]
    df = df.iloc[1:] #skip headers
    gene = f"PF3D7_{gene}"
    data[gene] = df
# for each gene get the studies and difference
all_rows = []
for gene, df in data.items():
    for _, row in df.iterrows():
        all_rows.append({
            "Gene": gene,
            "Study": normalize_study(str(row["Study"])),
            "Difference": abs(pd.to_numeric(row["Difference"], errors="coerce"))
        })

long_df = pd.DataFrame(all_rows)

cmap = ListedColormap(['green', 'gold', 'orange', 'red', 'maroon'])

# 0 green, (0,1] yellow, (1,2] orange, (2,3] orangered, >3 red
long_df["Bin"] = np.digitize(long_df["Difference"].to_numpy(), [0, 1, 2, 3], right=True)
counts_df = (
    long_df.dropna(subset=["Difference"])
    .groupby(["Gene", "Bin"])
    .size()
    .reset_index(name="Count")
)

bins_ordered = sorted(counts_df["Bin"].unique())

genes_ordered = list(data.keys())
n_genes = len(genes_ordered)

bar_width = 0.6

fig = plt.figure(figsize=(max(14, n_genes * 0.85), 28), constrained_layout=True)
gs = fig.add_gridspec(2, 2, height_ratios=[2.5, 1])
ax = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
fig.get_layout_engine().set(hspace=0.03, wspace=0.08, h_pad=0.2, w_pad=0.2)

## panel A
for gi, gene in enumerate(genes_ordered):
    gene_counts = counts_df[counts_df["Gene"] == gene].set_index("Bin")["Count"]
    bottom = 0
    for b in bins_ordered:
        count = gene_counts.get(b, 0)
        if count == 0:
            continue
        color = cmap(b)
        ax.bar(gi, count, width=bar_width, bottom=bottom, color=color, edgecolor="white", linewidth=0.5)
        bottom += count

ax.set_xticks(range(n_genes))
ax.set_xticklabels(genes_ordered, rotation=45, ha="right", fontsize=10)
ax.set_xlabel("Gene")
ax.set_ylabel("Number of Studies")
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

legend_elements = [
    Patch(facecolor="green", label="0"),
    Patch(facecolor="gold", label="≤1"),
    Patch(facecolor="orange", label="≤2"),
    Patch(facecolor="red", label="≤3"),
    Patch(facecolor="maroon", label=">3"),
]
ax.legend(handles=legend_elements, title="Score Difference", loc="upper left",
          bbox_to_anchor=(1.005, 1.02), fontsize=9, borderaxespad=0)
ax.text(-0.03, 1.05, "A", transform=ax.transAxes, fontsize=16, fontweight="bold")

## panel B
df2 = pd.read_csv("panels/comparison.csv")
df2 = df2.rename(columns={"Contradictions": "Observation Contradictions", "Contradictions.1": "Insight Contradictions"})
df2 = df2.drop(["Gene", "Tone", "Detail", "Headline", "Overall"], axis=1)
palette = ["lightcoral", "maroon", "coral", "red", "lightblue", "darkblue", "aqua", "dodgerblue"]

df2_long = df2.melt(var_name="Metric", value_name="Value")
sns.barplot(data=df2_long, x="Metric", y="Value", errorbar="sd", ax=ax2, palette=palette)
ax2.axvline(3.5, color="black", linestyle="--", linewidth=1)
ax2.text(-0.05, 1.05, "B", transform=ax2.transAxes, fontsize=16, fontweight="bold")
plt.setp(ax2.get_xticklabels(), rotation=20, ha="right", fontsize=10)

## panel C
df3 = pd.read_csv("panels/comparison.csv")
df3 = df3[["Tone", "Detail", "Headline", "Overall"]]

counts = df3.apply(pd.Series.value_counts).T
counts.plot(kind="bar", stacked=True, ax=ax3, color=["lightgreen", "darkgreen"])
ax3.set_xlabel("Metric")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)
label_map = {"A": "A = Original", "B": "B = Statistical"}
ax3.legend(labels=[label_map.get(c, c) for
                    c in counts.columns], title="Prompt version",
           loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=2, borderaxespad=0)
ax3.text(-0.05, 1.05, "C", transform=ax3.transAxes, fontsize=16, fontweight="bold")


plt.show()
fig.savefig("panels/AI_summ_panel2.png", dpi=600)
