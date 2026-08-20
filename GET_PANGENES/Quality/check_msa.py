import pandas as pd
df = pd.read_csv("all_clusters_quality_pseudo_v2.txt", sep="\t", header=None,
                 names=["file", "1stisof", "occup", "seqs", "mode_len", "SE_len",
                        "mode_exons", "SE_exons", "mode_dist", "max_dist", "SE_dist",
                        "sites", "Ca", "Cr_max", "Cr_min", "Cc_max", "Cc_min", "Cij_max", "Cij_min"])

print(df.head())
df["Gene"]=df["file"].str.split(".cdna").str[0]
print(df.head())

## overall ca
mean=df["Ca"].mean()
print(f"Mean:{mean}")
median=df["Ca"].median()
print(f"Median:{median}")

prod=pd.read_csv("product_des.txt", sep="\t")
#rif ca
rif=prod[prod["Product Description"].str.contains("rif|rifin",case=False)]
rif_list=rif["Gene ID"].to_list()
df_rif=df[df["Gene"].isin(rif_list)]
mean=df_rif["Ca"].mean()
print(f"Mean:{mean}")
median=df_rif["Ca"].median()
print(f"Median:{median}")
#var ca
var=prod[prod["Product Description"].str.contains("PfEMP1", case=False)]
var_list=var["Gene ID"].to_list()
df_var=df[df["Gene"].isin(var_list)]
mean=df_var["Ca"].mean()
print(f"Mean:{mean}")
median=df_var["Ca"].median()
print(f"Median:{median}")

### identify low msa completeness genes
prod_dict=dict(zip(prod["Gene ID"], prod["Product Description"]))
df["Product Description"]=df["Gene"].map(prod_dict)
print(df.head())
df_low=df[df["Ca"]<0.4]
print(len(df_low))
vc=df_low["Product Description"].value_counts().reset_index()
vc.columns=["Product Description","Count"]
vc=vc[vc["Product Description"].str.contains("unknown function")]
print(vc)
print(sum(vc["Count"]))