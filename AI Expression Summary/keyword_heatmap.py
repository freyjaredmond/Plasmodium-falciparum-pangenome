### The script used to plot a heatmap showing the difference between the language based magnitude score and the fold change percentile score
### A large difference indicates that the AI is over or understating the magnitude of change
### This was carried out on 10 random genes
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm

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
sheets = pd.read_excel("scores_excel_genes.xlsx", sheet_name=None)
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
study_labels={label:i+1 for i, label in enumerate(heatmap_df.columns)}
heatmap_df.columns = [study_labels[s] for s in heatmap_df.columns]
cmap = ListedColormap(['lightgreen', 'gold', 'orange', 'red'])
norm = BoundaryNorm([0, 1, 2, 3, 4], cmap.N) #alows you to make a colour pallete based of boundaries
fig,ax=plt.subplots(figsize=(15,15))
sns.heatmap(heatmap_df, cmap=cmap, norm=norm, ax=ax,  cbar_kws={"label": "Score Difference"})
ax.set_yticklabels(ax.get_yticklabels(),rotation=0, ha="right")
ax.set_xlabel("Study")

plt.show()
fig.savefig("keywords_heatmap.png", dpi=300)
