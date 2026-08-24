import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import os

nf_files = glob.glob("PSEUDO/unmapped_genes/*.txt")
matrix = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)

# map every individual gene ID to its cluster
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
    no_flank_data.append({"Genome": genome, "Unrecovered": counts})
ndf = pd.DataFrame(no_flank_data)

total_noflank = sum(ndf["Unrecovered"])
print(f"Sum of absent genes from 3D7 without flank parameter: {total_noflank}")

palette = ["darkgreen"]
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(data=ndf, x="Genome", y="Unrecovered", hue="Genome", palette=palette, ax=ax)
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

# identifying reference absent genes from the matrix
## clusters where 3D7 has no gene
absent_3d7_clusters = matrix.columns[matrix.loc["PlasmoDB-68_Pfalciparum3D7"] == "-"]
absent_3d7_matrix = matrix[absent_3d7_clusters]

print(f"Number of clusters missing 3D7: {len(absent_3d7_clusters)}")

genome_gene_counts = []
total_genes = 0
for genome in absent_3d7_matrix.index:
    count = 0
    for cell in absent_3d7_matrix.loc[genome]:
        if cell != "-":
            count += 1
    genome_gene_counts.append({"Genome": genome, "Pangene counts": count})
    total_genes += count

print(f"Total number of genes in clusters missing 3D7: {total_genes}")

genome_gene_df = pd.DataFrame(genome_gene_counts).sort_values("Pangene counts", ascending=False)

# clean genome names so they match ndf's format for merging
ndf["Genome"] = ndf["Genome"].str.upper()
genome_gene_df["Genome"] = genome_gene_df["Genome"].str.split("Pfalciparum").str[1].str.upper()

print("ndf genomes:", sorted(ndf["Genome"].unique()))
print("genome_gene_df genomes:", sorted(genome_gene_df["Genome"].unique()))

joined = ndf.merge(genome_gene_df, on="Genome")
joined["Recovered"] = joined["Pangene counts"] - joined["Unrecovered"]
print(joined)

#seperate recovered into valid orfs or not

lo_files = glob.glob("PSEUDO/Liftoff/*.gff3_polished")
total_genes = 0
table_data = []

for files in lo_files:
    genome = os.path.basename(files).split("_")[0]
    valid = 0
    invalid = 0

    df = pd.read_csv(files, sep="\t", skiprows=3, header=None)
    df2 = df[df[2] == "gene"]

    for _, row in df2.iterrows():
        if "valid_ORFs=1" in row[8]:
            valid += 1
            total_genes += 1
        else:
            invalid += 1

    table_data.append({"Genome": genome, "Invalid": invalid, "Valid": valid})

print(f"Number of genes with valid ORFs: {total_genes}")

liftoff_df = pd.DataFrame(table_data)


liftoff_df["Genome"] = liftoff_df["Genome"].str.upper()

joined = joined.merge(liftoff_df, on="Genome")


plot_df = joined[["Genome", "Pangene counts", "Valid", "Invalid", "Unrecovered"]].rename(columns={
    "Pangene counts": "Absent in Pangenome",
    "Valid": "Recovered: Valid ORF",
    "Invalid": "Recovered: Invalid ORF",
})

category_order = ["Absent in Pangenome", "Recovered: Valid ORF", "Recovered: Invalid ORF", "Unrecovered"]
melted = plot_df.melt(id_vars="Genome", value_vars=category_order, var_name="Category", value_name="Count")

fig3, ax3 = plt.subplots(figsize=(16, 8))
sns.barplot(data=melted, x="Genome", y="Count", hue="Category", hue_order=category_order, ax=ax3)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha="right")
ax3.set_xlabel("Genome")
ax3.set_ylabel("Count")
ax3.legend(title=None, loc="upper left", bbox_to_anchor=(1.02, 1))
fig3.subplots_adjust(bottom=0.3, right=0.8)
fig3.savefig("PSEUDO/Graphs/pangene_recovery_by_genome.png", dpi=300, bbox_inches="tight")
plt.show()
