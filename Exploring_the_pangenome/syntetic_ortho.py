import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

ortho = pd.read_csv("PSEUDO/syntetic_orthos.txt", sep="\t")

# Build a graph: every gene is a node, every ortholog relationship is an edge
G = nx.Graph()
G.add_nodes_from(ortho["Gene ID"])  # every gene gets added, even ones with no orthologs

for _, row in ortho.iterrows():
    gene_a = row["Gene ID"]
    partners_raw = row["Input Ortholog(s)"]
    # genes with no orthologs
    if pd.isna(partners_raw):
        continue
    for gene_b in partners_raw.split(","):
        G.add_edge(gene_a, gene_b.strip())

# Find the clusters- includes genes with no orthologs
clusters = list(nx.connected_components(G))
print("Total ortholog clusters:", len(clusters))

#map to the product descriptions
#select 3d7 gene were possible as will have better annotations
def get_representative(cluster_genes):
    cluster_list = sorted(cluster_genes)
    pf3d7_genes = [g for g in cluster_list if g.startswith("PF3D7_")]
    if pf3d7_genes:
        return pf3d7_genes[0]
    return cluster_list[0]
prod=pd.read_csv("PSEUDO/product_des.txt", sep="\t")
prod_map=dict(zip(prod["Gene ID"], prod["Product Description"]))
results = []
for comp in clusters:
    rep_gene = get_representative(comp)
    rep_product = prod_map.get(rep_gene)
    results.append({
        "cluster_size": len(comp),
        "representative_gene": rep_gene,
        "product_description": rep_product
    })

results_df = pd.DataFrame(results)
print(results_df.head())


# split into var and rif


## rif
rif_df=results_df[results_df["product_description"].str.contains("rifin|rif", case=False, na=False)]
rif_clusters=len(rif_df)
print(len(rif_df))
print(f"Max={max(rif_df["cluster_size"])}")
print(f"Min={min(rif_df["cluster_size"])}")

## var
var_df=results_df[results_df["product_description"].str.contains("erythrocyte membrane protein 1, PfEMP1|var", case=False, na=False)]
var_clusters=len(var_df)
print(len(var_df))
print(f"Max={max(var_df["cluster_size"])}")
print(f"Min={min(var_df["cluster_size"])}")

## stevor
stevor_df=results_df[results_df["product_description"].str.contains("stevor", case=False, na=False)]
stevor_clusters=len(stevor_df)
print(len(stevor_df))
print(f"Max={max(stevor_df["cluster_size"])}")
print(f"Min={min(stevor_df["cluster_size"])}")


## get_pangenes counts
## get_pangenes counts
matrix = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)

col_oc = []
for cluster_id in matrix.columns:
    occupancy = (matrix[cluster_id] != "-").sum()
    if occupancy == 1:
        continue
    col_oc.append({"Cluster": cluster_id,
                    "Occupancy": occupancy})

df2 = pd.DataFrame(col_oc)
df2["Product Description"] = df2["Cluster"].map(prod_map)

## rif
rif_df2 = df2[df2["Product Description"].str.contains("rifin|rif", case=False, na=False)]
rif_clusters2 = len(rif_df2)
print(len(rif_df2))
print(f"Max={max(rif_df2['Occupancy'])}")
print(f"Min={min(rif_df2['Occupancy'])}")

## var
var_df2 = df2[df2["Product Description"].str.contains("erythrocyte membrane protein 1, PfEMP1|var", case=False, na=False)]
var_clusters2 = len(var_df2)
print(len(var_df2))
print(f"Max={max(var_df2['Occupancy'])}")
print(f"Min={min(var_df2['Occupancy'])}")

## stevor
stevor_df2 = df2[df2["Product Description"].str.contains("stevor", case=False, na=False)]
stevor_clusters2 = len(stevor_df2)
print(len(stevor_df2))
print(f"Max={max(stevor_df2['Occupancy'])}")
print(f"Min={min(stevor_df2['Occupancy'])}")

## summary table for plotting 
family_counts = pd.DataFrame([
    {"gene_family": "rifin",  "method": "PlasmoDB", "cluster_count": rif_clusters},
    {"gene_family": "rifin",  "method": "GET_PANGENES",           "cluster_count": rif_clusters2},
    {"gene_family": "var",    "method": "PlasmoDB", "cluster_count": var_clusters},
    {"gene_family": "var",    "method": "GET_PANGENES",           "cluster_count": var_clusters2},
    {"gene_family": "stevor", "method": "PlasmoDB", "cluster_count": stevor_clusters},
    {"gene_family": "stevor", "method": "GET_PANGENES",           "cluster_count": stevor_clusters2},
])
print(family_counts)
family_counts.to_csv("PSEUDO/synteny_vs_getpangenes_family_counts.tsv", sep="\t", index=False)

## plot 
method_colours = {"PlasmoDB": "red", "GET_PANGENES": "orange"}

families = ["rifin", "var", "stevor"]
methods = ["PlasmoDB", "GET_PANGENES"]

x = range(len(families))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))
for i, method in enumerate(methods):
    counts = [family_counts.loc[(family_counts["gene_family"] == fam) &
                                 (family_counts["method"] == method),
                                 "cluster_count"].iloc[0] for fam in families]
    offset = (i - 0.5) * width
    ax.bar([xi + offset for xi in x], counts, width=width,
           color=method_colours[method], label=method)

ax.set_xticks(list(x))
ax.set_xticklabels(families)
ax.set_xlabel("Gene family")
ax.set_ylabel("Cluster count")
ax.legend()
fig.tight_layout()
fig.savefig("PSEUDO/GRAPHS/family_cluster_counts_by_method.png", dpi=300, facecolor="white")
plt.show()