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

### map the reference-absent genes to their pangenome cluster
absent_clusters = []
unmatched = []
for gene in no_flank_list:
    cluster = gene_to_cluster.get(gene)
    if cluster is not None:
        absent_clusters.append(cluster)
    else:
        unmatched.append(gene)

print(f"Reference-absent genes matched to a cluster: {len(absent_clusters)}")
print(f"Reference-absent genes with no cluster match: {len(unmatched)}")

cluster_counts = pd.Series(absent_clusters).value_counts()
print(f"Clusters containing at least one reference-absent gene: {len(cluster_counts)}")

genes_per_cluster = cluster_counts.value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
bar = ax2.bar(genes_per_cluster.index.astype(str), genes_per_cluster.values, color="darkgreen")
ax2.set_xlabel("Reference-absent genes per cluster")
ax2.set_ylabel("Number of clusters")
ax2.bar_label(bar)
fig2.savefig("PSEUDO/Graphs/reference_absent_genes_per_cluster.png", dpi=300, bbox_inches="tight")
plt.show()
