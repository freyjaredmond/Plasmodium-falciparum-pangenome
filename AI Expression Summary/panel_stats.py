# a script to plot the stats analysis, panel A= magnitude of change comparison, B= observation counts and C= preffered detail
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm

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
#make long for heatmap- also puts the same study in the same column
heatmap_df = long_df.pivot(index="Gene", columns="Study", values="Difference")
print(long_df["Difference"].value_counts())
study_labels={label:i+1 for i, label in enumerate(heatmap_df.columns)}
heatmap_df.columns = [study_labels[s] for s in heatmap_df.columns]
cmap = ListedColormap(['lightgreen', 'gold', 'orange', 'red'])
norm = BoundaryNorm([0, 1, 2, 3, 4.0001], cmap.N) #alows you to make a colour pallete based of boundaries
fig = plt.figure(figsize=(11, 10))
gs = fig.add_gridspec(2, 2, hspace=0.4, bottom=0.25, left=0.2)
ax = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])

sns.heatmap(heatmap_df, cmap=cmap, norm=norm, ax=ax,  cbar_kws={"label": "Score Difference"})
cbar = ax.collections[0].colorbar
cbar.set_ticks([0, 1, 2, 3, 4])
cbar.set_ticklabels(["0", "1", "2", "3", "4"])
ax.set_yticklabels(ax.get_yticklabels(),rotation=0, ha="right")
ax.set_xlabel("Study")
ax.tick_params(axis="both", labelsize=10)
ax.text(-0.05, 1.05, "A", transform=ax.transAxes, fontsize=16, fontweight="bold")

## panel B
df2=pd.read_csv("panels/comparison.csv")
df2=df2.rename(columns={"Contradictions": "Observation Contradictions", "Contradictions.1": "Insight Contradictions"})
df2=df2.drop(["Gene","Tone","Detail","Headline","Overall"], axis=1)
palette=["lightcoral","maroon","coral","red","lightblue","darkblue","aqua","dodgerblue"]

df2_long = df2.melt(var_name="Metric", value_name="Value")
print(df2_long.head())
sns.barplot(data=df2_long, x="Metric", y="Value", errorbar="sd", ax=ax2, palette=palette)
ax2.axvline(3.5, color="black", linestyle="--", linewidth=1)
ax2.text(-0.05, 1.05, "B", transform=ax2.transAxes, fontsize=16, fontweight="bold")
plt.setp(ax2.get_xticklabels(), rotation=20, ha="right", fontsize=10)
###c
df3=pd.read_csv("panels/comparison.csv")
df3=df3[["Tone","Detail","Headline","Overall"]]

counts = df3.apply(pd.Series.value_counts).T
print(counts)
counts.plot(kind="bar", stacked=True, ax=ax3, color=["lightgreen","darkgreen"])
ax3.set_xlabel("Metric")
ax3.set_ylabel("Count")
ax3.tick_params(axis="x", rotation=0)
label_map = {"A": "A = Original", "B": "B = Statistical"}
ax3.legend(labels=[label_map.get(c, c) for
                    c in counts.columns], title="Prompt version",
           loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=2, borderaxespad=0)
ax3.text(-0.05, 1.05, "C", transform=ax3.transAxes, fontsize=16, fontweight="bold")


plt.show()
fig.savefig("panels/AI_summ_panel.png", dpi=600)

