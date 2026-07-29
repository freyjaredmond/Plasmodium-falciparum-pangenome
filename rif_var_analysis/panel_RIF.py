import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
import io
from PIL import Image
import seaborn as sns
import scipy.stats as stats
from scipy.stats import levene, kruskal, chi2_contingency
import scikit_posthocs as sp

 
fig = plt.figure(figsize=(12, 14))
gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[1, 1,1],
                       width_ratios=[1, 1], hspace=0.25, wspace=0.1)
ax_a = fig.add_subplot(gs[0, :])
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[1, 1])
ax_d = fig.add_subplot(gs[2, :])

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

rif_fasta = glob.glob("GET_PANGENES_pseudo/rif_analysis/rif_fasta_finished/*fasta")
fheyder_results = []
#read every rif fasta
for fasta in rif_fasta:
    genome = os.path.basename(fasta).split("_")[0]
    current_id = None
    current_seq = []
    
    with open(fasta, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                # process previous sequence
                if current_id and current_seq:
                    seq = "".join(current_seq).upper()
                    fheyder_results.append({
                        "Genome": genome,
                        "Gene": current_id,
                        "has_FHEYDER": "FHEYDER" in seq #get sequences with the FHEYDER motif
                    })
                current_id = line.replace(">", "").strip()
                current_seq = []
            else:
                current_seq.append(line)
        # process last sequence
        if current_id and current_seq:
            seq = "".join(current_seq).upper()
            fheyder_results.append({
                "Genome": genome,
                "Gene": current_id,
                "has_FHEYDER": "FHEYDER" in seq
            })

fheyder_df = pd.DataFrame(fheyder_results)
fheyder_df.to_csv("PSEUDO/fheyder_genes.tsv", sep="\t")
print(fheyder_df.head())
#get the genome counts
per_genome = fheyder_df.groupby("Genome")["has_FHEYDER"].sum().reset_index()
per_genome.columns = ["Genome", "FHEYDER_count"]
print(per_genome)
per_genome.to_csv("PSEUDO/fheyder_counts.tsv", sep="\t", index=False)

#### get the table with rif subtypes and merge on
rif_types=pd.read_csv("PSEUDO/rif_types_with_consistency.tsv", sep="\t")
print(rif_types.head())
merged_df=rif_types.merge(fheyder_df, on=["Genome","Gene"])
print(merged_df.head())

#label the rifinA type to include FHEYDER
def change_type(row):
    if row["has_FHEYDER"] == True:
        return f"{row['Type']}(FHEYDER)"
    else:
        return row["Type"]

merged_df["Type"] = merged_df.apply(change_type, axis=1)

merged_df=merged_df.drop(["Consistency","Most_common_type"], axis=1)
#recaluclate consistency
#get the percentage of genes within a cluster that have the same type
cluster_consistency = merged_df.groupby("Cluster")["Type"].agg(
    lambda x: x.value_counts().iloc[0] / len(x)
).reset_index()
cluster_consistency.columns = ["Cluster", "Consistency"]

#get the name of the most common type

cluster_type = merged_df.groupby("Cluster")["Type"].agg(
    lambda x: x.value_counts().index[0]
).reset_index()
cluster_type.columns = ["Cluster", "Most_common_type"]

#merge the dfs
final_df = merged_df.merge(cluster_consistency, on="Cluster")
final_df = final_df.merge(cluster_type, on="Cluster")
final_df.to_csv("PSEUDO/rif_types_fheyder_with_consistency.tsv", sep="\t")

#get consistency >=0.75
final_df_filtered=final_df[final_df["Consistency"]>=0.75]
vc=final_df_filtered["Consistency"].value_counts().reset_index()
vc.columns=["Consistency","Counts"]
vc.to_csv("PSEUDO/consistency_fheyder.tsv", sep="\t")
print(vc)

#drop dups
df_clusters = final_df_filtered.drop_duplicates(subset=["Cluster"])
###
print(df_clusters["Consistency"].value_counts())
vc=df_clusters["Consistency"].value_counts().reset_index()
vc.columns=["Consistency","Counts"]
vc.to_csv("PSEUDO/fheyder_cluster_consistency_stats.txt", sep="\t")
#get the number of each type for each occupancy
grouped = df_clusters.groupby(["Occupancy", "Most_common_type"]).size().reset_index(name="count")
pivot = grouped.pivot(index="Occupancy", columns="Most_common_type", values="count").fillna(0)

##plot

pivot.plot(kind="bar", stacked=True, ax=ax_a, color=["steelblue", "green","firebrick"])
ax_a.set_xlabel("Occupancy")
ax_a.set_ylabel


import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations

matrix = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)
cassettes = pd.read_csv("GET_PANGENES_pseudo/Var_analysis/domain_matches/domain_assignemnts.tsv", sep="\t")

# cassettes per genome
cassettes_only = cassettes[cassettes["Cassette"] != "no_cassette"]
print(cassettes_only["Cassette"].value_counts())
grouped = cassettes_only.groupby(["Genome", "Cassette"]).size().reset_index(name="count")
grouped.to_csv("PSEUDO/genome_dc_grouped.csv", sep="\t")
print(len(cassettes_only[cassettes_only["Cassette"]=="DC4"]))
# interesting cassettes
interesting_cassettes=cassettes_only[cassettes_only["Cassette"].isin(["DC13","DC8","DC11","DC15","DC4"])]
grouped2 = interesting_cassettes.groupby(["Genome", "Cassette"]).size().reset_index(name="count")
print(grouped2)

#get locations
geo_map = {"3D7":"West Africa", "NF54":"West Africa", "CD01":"Central Africa",
           "GA01":"Central Africa", "GN01":"West Africa", "GB4":"West Africa",
           "NF166":"West Africa", "SN01":"West Africa", "KE01":"East Africa",
           "7G8":"South America", "7G8-2019":"South America", "HB3":"Central America",
           "DD2":"Southeast Asia", "KH01":"Southeast Asia", "KH02":"Southeast Asia",
           "IT":"Southeast Asia"}

region_colours = {"West Africa": "lightblue", 
                  "East Africa": "lightgreen",
                  "Central Africa":"orange",
                  "Central America":"grey",
                  "South America": "lightsalmon", 
                  "Southeast Asia": "yellow"}
#make wide for plotting

pivot = grouped2.pivot(index="Genome", columns="Cassette", values="count").fillna(0)

order = ["3D7", "NF54", "GN01", "GB4", "NF166", "SN01", "CD01","GA01", 
         "KE01", "7G8", "7G8-2019", "HB3", "DD2", "KH01", "KH02", "IT"]

# reindex to enforce order
pivot = pivot.reindex(order)
pivot.plot(kind="bar", stacked=True, ax=ax_d)
ax_d.set_xlabel("Genome")
ax_d.set_ylabel("Count")
for i, label in enumerate(ax_d.get_xticklabels()):
    genome = label.get_text()
    region = geo_map.get(genome, "Unknown")
    ax_d.get_xticklabels()[i].set_backgroundcolor(region_colours[region])
    # Geographic region legend
legend_patches = [Patch(facecolor=color, label=region) 
                  for region, color in region_colours.items()]
geo_legend = ax_d.legend(handles=legend_patches, title="Geographic Region", 
                          bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
ax_d.add_artist(geo_legend) #saves this legend then allows you to add another

# Cassette colour legend (matplotlib auto-generates this from the stacked bar)
ax_d.legend(title="Domain Cassette", bbox_to_anchor=(1.01, 0.5), loc='upper left', borderaxespad=0)

#jacarrd similairity function
def jaccard_similarity(domains1, domains2):
    set1 = set(domains1.split("|"))
    set2 = set(domains2.split("|")) #the number of genes in common/total genes available across paires
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0


def cluster_domain_consistency(genes_in_cluster, gene_domain_dict):
    domain_lists = [gene_domain_dict[gene] for gene in genes_in_cluster
                    if gene in gene_domain_dict] #get the domains for every gene in that cluster
    if len(domain_lists) == 1:
        return 1.0  # single gene consistent with itself
    similarities = [jaccard_similarity(a, b) for a, b in combinations(domain_lists, 2)] #combinations runs it in all combos
    return sum(similarities) / len(similarities)  # mean pairwise similarity

cluster_results = []

# create gene to assignment lookup
gene_assignment_dict = dict(zip(cassettes["Gene"], cassettes["Assignment"]))
gene_domain_dict= dict(zip(cassettes["Gene"], cassettes["Domains"]))

for col in matrix.columns:
    genes_in_cluster = []
    for gene in matrix[col]:
        if gene != "-":
            if ";" in str(gene):
                genes_in_cluster.append(str(gene).split(";")[0])  # take first gene only
            else:
                genes_in_cluster.append(gene)
    
    occupancy = len(genes_in_cluster)
  

    if occupancy == 0:
        continue

    # get assignments only for genes that made it through the pipeline
    assignments = [gene_assignment_dict[gene] for gene in genes_in_cluster
                   if gene in gene_assignment_dict]

    if len(assignments) == 0:
        continue

    counts = pd.Series(assignments).value_counts()
    most_common_val = counts.index[0]
    most_common_counts=counts.values[0]
    cassette_total=most_common_counts/len(assignments)

    consistency = cluster_domain_consistency(genes_in_cluster,gene_domain_dict)

    cluster_results.append({
        "Cluster": col,
        "Matrix_occupancy": occupancy,           # total genes in cluster from matrix
        "Genes_with_data": len(assignments),      # genes with pipeline assignments
        "Assignment": most_common_val,
        "Consistency_rate": consistency,
        "Cassette consistency":most_common_counts,
        "Cassette total":cassette_total  # out of genes with data
    })

cluster_df = pd.DataFrame(cluster_results)
cluster_df = cluster_df.sort_values("Cassette consistency", ascending=False)
print("Cluster")
print(cluster_df["Matrix_occupancy"].value_counts())

print(cluster_df.head(20))
conserved_assignment=cluster_df[(cluster_df["Cassette total"]==1) & (cluster_df["Genes_with_data"]!=1)]
conserved_assignment.to_csv("PSEUDO/conserved_assignments.tsv", sep="\t", index=False)

high_consistency=cluster_df[(cluster_df["Consistency_rate"]>0.5) & (cluster_df["Genes_with_data"]!=1)]
high_consistency.to_csv("PSEUDO/consistency_rate.tsv", sep="\t", index=False)

cluster_df.to_csv("PSEUDO/cluster_cassette_assignments.tsv",
                  sep="\t", index=False)

cluster_df_no_singleton=cluster_df[cluster_df["Genes_with_data"]!=1]
grouped3=cluster_df_no_singleton.groupby("Genes_with_data")["Consistency_rate"].apply(list)

bp=ax_b.boxplot(grouped3.values, labels=grouped3.index, patch_artist=True)
ax_b.set_xlabel("Occupancy")
ax_b.set_ylabel("Mean Jaccard Similarity")
for patch in bp["boxes"]:
    patch.set_facecolor("darkgreen")
    patch.set_alpha(0.7)



cassette_genome_occupancy = cassettes.groupby("Assignment")["Genome"].nunique().reset_index()
cassette_genome_occupancy.columns = ["Cassette", "Genome_count"]
cassette_genome_occupancy = cassette_genome_occupancy.sort_values("Genome_count", ascending=False)
cassette_genome_occupancy_filtered=cassette_genome_occupancy[cassette_genome_occupancy["Genome_count"]>=5]

print(len(cassette_genome_occupancy_filtered))
print(cassette_genome_occupancy_filtered)
cassette_genome_occupancy_filtered["Cassette"] = cassette_genome_occupancy_filtered["Cassette"].replace(
    "NTSB3|DBLa0.11|CIDRa2.4|DBLd1|CIDRb1|ATSB1", "Unclassified"
)



colors = ["lightgreen","darkgreen"]
ax_c.bar(cassette_genome_occupancy_filtered["Cassette"], cassette_genome_occupancy_filtered["Genome_count"], color=colors)
ax_c.set_xlabel("Cassette/Domain combination")
ax_c.set_ylabel("Count")
ax_c.set_xticks(range(len(cassette_genome_occupancy_filtered["Cassette"])))
ax_c.set_xticklabels(cassette_genome_occupancy_filtered["Cassette"], rotation=45, ha="right")

ax_a.text(-0.01, 1.07, 'A', transform=ax_a.transAxes, fontsize=14, fontweight='bold', va='top', ha='right')
ax_b.text(-0.05, 1.07, 'B', transform=ax_b.transAxes, fontsize=14, fontweight='bold', va='top', ha='right')
ax_c.text(0, 1.07, 'C', transform=ax_c.transAxes, fontsize=14, fontweight='bold', va='top', ha='right')
ax_d.text(0, 1.07, 'D', transform=ax_d.transAxes, fontsize=14, fontweight='bold', va='top', ha='right')

fig.subplots_adjust(left=0.08, right=0.97, top=0.97, bottom=0.1)
fig.savefig("PSEUDO/Graphs/panel_rif_var.png", dpi=300, facecolor="white", bbox_inches="tight")
plt.show()