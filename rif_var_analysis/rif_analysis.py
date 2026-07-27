## A script to assign rifin subtypes (results taken from STRIDE) to each pangene. 
## The occupancy of the rifin subtypes was plotted across pangenome occupancies 
## Statistical analysis was perfomed to determine whether rifin subtype is associated 
## with pangenome occupancy
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
matrix=pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t")
# get an occupancy function
def get_occupancy(input_gene, matrix):
    for col in matrix.columns:
        cluster_genes=[]
        for gene in matrix[col]:
            if gene!="-":
                if ";" in str(gene):
                    gene=str(gene).split(";")[0]
                    cluster_genes.append(gene)
                else:
                  cluster_genes.append(gene)
        if input_gene in cluster_genes:  # found the right cluster
            return col,len(cluster_genes)
    return None  # gene not in matrix

#get the type mapped to occupancy

stride_files=glob.glob("GET_PANGENES_pseudo/rif_analysis/rif_annotated/*txt")
rif_data=[]
for stride in stride_files:
    genome=os.path.basename(stride).split(".")[1].replace("_rif","")
    stride_data=pd.read_csv(stride, sep="\t")
    for idx, rows in stride_data.iterrows():
        gene_id=rows.iloc[0]
        gene_id=gene_id.strip()
        rif_type=rows.iloc[1]
        if "Unlikely" in rif_type:
            continue
        if "like"in rif_type:
            continue
        if "likely" in rif_type:
            continue
        if "-"not in rif_type:
            continue
        result = get_occupancy(gene_id, matrix)
        if result is None:
            continue  # skip genes not in matrix
        cluster, occupancy = result

        rif_data.append({"Genome":genome,
                        "Gene":gene_id,
                        "Type":rif_type,
                        "Cluster":cluster,
                        "Occupancy":occupancy})
df=pd.DataFrame(rif_data)
print(df.head())
print(len(df))

df.to_csv("PSEUDO/rif_analysis/rif_results/rifs_including_stevor.tsv", sep="\t")
# remove stevors
df_filtered=df[df["Type"]!="STEVOR"]
print(len(df_filtered))

#get the percentage of genes within a cluster that have the same type
cluster_consistency = df_filtered.groupby("Cluster")["Type"].agg(
    lambda x: x.value_counts().iloc[0] / len(x)
).reset_index()
cluster_consistency.columns = ["Cluster", "Consistency"]

#get the name of the most common type

cluster_type = df_filtered.groupby("Cluster")["Type"].agg(
    lambda x: x.value_counts().index[0]
).reset_index()
cluster_type.columns = ["Cluster", "Most_common_type"]

#merge the dfs
df_filtered = df_filtered.merge(cluster_consistency, on="Cluster")
df_filtered = df_filtered.merge(cluster_type, on="Cluster")

#save
df_filtered.to_csv("PSEUDO/rif_types_with_consistency.tsv", sep="\t")

### Identify the FHEYDER motif using exact string matching
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
fig, ax = plt.subplots(figsize=(12, 6))
pivot.plot(kind="bar", stacked=True, ax=ax, color=["steelblue", "green","firebrick"])
ax.set_xlabel("Occupancy")
ax.set_ylabel("Count")
plt.show()
fig.savefig("PSEUDO/Graphs/rif_type_occupancy_fheyder.png", dpi=300)
pivot.to_csv("PSEUDO/counts_per_occupancy.tsv", sep="\t")


#stats
from scipy.stats import chi2_contingency

# group i
def occ_group(occ):
    if occ == 1:
        return "singleton"
    elif occ <= 4:
        return "low (2-4)"
    else:
        return "high (5+)"

df_clusters["occ_group"] = df_clusters["Occupancy"].apply(occ_group)

contingency = pd.crosstab(df_clusters["occ_group"], df_clusters["Most_common_type"]) #cross tab gets frequency of each group
print(contingency)
chi2, p, dof, expected = chi2_contingency(contingency)
print(f"Chi-square: {chi2:.3f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of freedom: {dof}")

