import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import os

nf_files = glob.glob("PSEUDO/unmapped_genes/*.txt")
matrix = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)

# map every individual gene ID (splitting duplicate copies) to its cluster
gene_to_cluster = {}
for col in matrix.columns:
    for cell in matrix[col]:
        if cell != "-":
            for gene in cell.split(","):
                gene_to_cluster[gene] = col

#no flank
no_flank_data = []
no_flank_list = []
for file in nf_files:
    file_data = pd.read_csv(file, sep="\t", header=None, names=["Gene ID"])
    file_name = os.path.basename(file)
    genome = file_name.split("_")[0]
    counts = len(file_data)
    for gene in file_data["Gene ID"]:
        no_flank_list.append(gene)
    no_flank_data.append({"Genome": genome, "Counts": counts})
ndf = pd.DataFrame(no_flank_data)

total_noflank = sum(ndf["Counts"])
print(f"Sum of absent genes from 3D7 without flank parameter: {total_noflank}")

palette=["lightgreen", "darkgreen"]
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(data=ndf,
            x="Genome",
            y="Counts",
            hue="Genome",
            palette=palette,
            ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_xlabel("Genome")
fig.subplots_adjust(bottom=0.3)
fig.savefig("PSEUDO/Graphs/no_flank_unmapped.png", bbox_inches="tight")
plt.show()

