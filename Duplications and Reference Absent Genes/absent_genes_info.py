import pandas as pd
import glob
import os

data = pd.read_csv("PSEUDO/no_flank_unmapped_product_des", sep="\t")
gene_list=data["Gene ID"].to_list()

gff_data = []
gff_files = glob.glob("GET_PANGENES_filtered/inputs_flat/*gff")

for gff in gff_files:
    file_name = os.path.basename(gff)
    genome = file_name.split("Pfalciparum")[1].replace(".gff", "")
    
    with open(gff, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) < 9:
                continue
            if parts[2] in ["gene", "pseudogene"]:
                gene_id = parts[8].split(";")[0].split("ID=")[1]
                if gene_id in gene_list:
                    chromosome = parts[0]
                    start = parts[3]
                    end = parts[4]
                    gff_data.append({"Gene ID": gene_id,
                                    "Genome": genome,
                                    "Chromosome": chromosome,
                                    "Start Position": start,
                                    "End Position": end})
                else:
                    continue
df1 = pd.DataFrame(gff_data)
df2 = df1.merge(data, on="Gene ID", how="inner")
print(df2)
if len(df1)!=len(df2):
    print("Matching error")
else:
    print("Same length")


### add occupancy information
matrix=pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)
occupancy_data=[]
for col in matrix.columns:
    occupancy = 0
    genes_in_cluster = []
    genes_unmapped = 0
    genes_unmapped_list = []
    
    for cell in matrix[col]:
        if cell != "-":
            occupancy += 1
            genes_in_cluster.extend(cell.split(","))
            for gene in cell.split(","):
                if gene in gene_list:
                    genes_unmapped += 1
                    genes_unmapped_list.append(gene)


    for gene in genes_unmapped_list:
        occupancy_data.append({
            "Gene ID": gene,
            "Cluster": col,
            "Occupancy": occupancy,
            "Genes in cluster": genes_in_cluster,
            "Number of genes unmapped": genes_unmapped,
            "Percentage of genes unmapped": (genes_unmapped / occupancy) * 100,
            "Genes unmapped": genes_unmapped_list
        })
df3=pd.DataFrame(occupancy_data)
final_df=df2.merge(df3, on="Gene ID", how="inner")

if len(df1)!=len(df3):
    print("Matching error")
else:
    print("Same length")

final_df.to_csv("PSEUDO/no_flank_unmapped_genes.tsv", sep="\t")
with open("PSEUDO/no_flank_liftoff_stats.tsv", "w") as f:
    f.write("Occupancy\n")
    f.write(10*"-" + "\n")
    f.write(final_df["Occupancy"].value_counts().to_string() + "\n")
    f.write(10*"-" + "\n")
    f.write("Percentage unmapped\n")
    f.write(10*"-" + "\n")
    f.write(final_df["Percentage of genes unmapped"].value_counts().to_string() + "\n")

### Extract the 58 genes that have 100% unmapped in a cluster (not cloud)
shell_df = final_df[(final_df["Occupancy"] != 1) & (final_df["Percentage of genes unmapped"] == 100)]

print(shell_df[["Cluster","Occupancy"]])

print(shell_df["Product Description"].value_counts())

shell_df.to_csv("PSEUDO/no_flank_shell_genes_of_interest.tsv", sep="\t")

hypo_shell_df=shell_df[shell_df["Product Description"].isin(["hypothetical protein"])]

print(hypo_shell_df)

hypo_shell_df.to_csv("PSEUDO/no_flank_hypo_shell_of_interest.csv", sep=",")

