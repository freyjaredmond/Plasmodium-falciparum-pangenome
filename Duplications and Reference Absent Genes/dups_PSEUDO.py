import pandas as pd
matrix = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)
data = []
for col in matrix.columns:
    for gene in matrix[col]:
        if gene != "-" and "," in str(gene):
            data.append({"Cluster": col, "Gene": gene})
df = pd.DataFrame(data)
df.to_csv("PSEUDO/duplications_PSEUDO.tsv", sep="\t", index=False)
print(len(df))
print(df.head())
print(len(df["Cluster"].unique()))
