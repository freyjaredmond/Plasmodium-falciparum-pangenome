import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from scipy import stats
from scipy.stats import kruskal
import scikit_posthocs as sp
import glob
import numpy as np
data_3d7=pd.read_csv("Functional_analysis/Alphafold/Alphafold_analysis/Alphafold_stats_from_tar.csv", sep=",", index_col=False)
data_non=pd.read_csv("Functional_analysis/Alphafold/Alphafold_analysis/Alphafold_stats_from_tar_non3d7.csv", sep=",", index_col=False)
df=pd.concat([data_3d7, data_non], ignore_index=True)
print(df.head())
df.to_csv("pLDDT_scores_pangenes.tsv", sep="\t")
#match uniprot to mean plddt
uni_plddt=dict(zip(df['id'], df['mean_plddt']))

#match uniprot id to gene id
uni_id=list(uni_plddt.keys())
clean_dict={}


for id in uni_id:
    parts = id.split("-")
    if len(parts) > 1:
        clean_id = parts[1]
        clean_dict[clean_id] = uni_plddt[id]
    else:
        print("Unexpected format:", id)  # see what's causing it
        clean_dict[id] = uni_plddt[id] 

uni_prot_data=pd.read_csv("Functional_analysis/uniprot_id.txt", sep="\t")
gene_uniprot=dict(zip(uni_prot_data["Gene ID"], uni_prot_data["UniProt ID(s)"]))

#get plddt for each gene
gene_plddt={}
gene_no_uni=[]
for gene, uni in gene_uniprot.items():
    unis=str(uni).split(",")
    matched=False
    for u in unis:
        if u in clean_dict:
            gene_plddt[gene]=clean_dict[u]
            matched=True
            break
    if not matched:
            gene_plddt[gene]=None
            gene_no_uni.append(gene)

#check if any gene in the AF file has not been matched
gene_list=df["id"].tolist()
genes_missing=[]
missing_count=0
for gene in gene_no_uni:
     if gene in gene_list:
          genes_missing.append(gene)
          missing_count+=1
          
print(f"Number of genes missing:{missing_count}")

###match plddt data and uniprot id to pangenes matrix
matrix=pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)


matrix_data=[]
#create occupancy matrix
for cluster in matrix.columns:
    occupancy = (matrix[cluster] != "-").sum() 
    if occupancy==16:
        group="Core"
    elif occupancy==15:
        group="Soft-core"
    elif occupancy in (1,2):
        group="Cloud"
    else:
        group="Shell"
    uniprot_id = gene_uniprot.get(cluster)
    plddt = gene_plddt.get(cluster)
    matrix_data.append({"Pangene":cluster,
                        "Occupancy":occupancy,
                        "Group":group,
                        "UniProt ID":uniprot_id,
                        "Mean_pLDDT": plddt})
df2=pd.DataFrame(matrix_data)



#group by occupancy
df2_grouped = df2.groupby("Occupancy")["Mean_pLDDT"].mean()
print(df2_grouped)

print(df2.value_counts("Group").dropna())

#plot the results
colours_dict = {
    "Core": "red",
    "Soft-core": "orange",
    "Shell": "green",
    "Cloud": "blue"
}
order=["Cloud","Shell","Soft-core","Core"]
fig,ax=plt.subplots(figsize=(12,6))
g=sns.violinplot(data=df2,
              x=df2["Group"],
              y=df2["Mean_pLDDT"],
              hue=df2["Group"],
              palette=colours_dict,
              ax=ax,
              legend=False,
              inner="box",
              fill=True,
              alpha=0.4,
              order=order)
ax.set_xlabel("Pangene Occupancy")
ax.set_ylabel("Mean pLDDT")

legend_elements = [
    Patch(facecolor="red", alpha=0.7, label="Core"),    
    Patch(facecolor="orange", alpha=0.7, label="Soft-core"),
    Patch(facecolor="green", alpha=0.7, label="Shell"),
    Patch(facecolor="blue", alpha=0.7, label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right") #use bbox to anchor to move the key out
plt.show()
fig.savefig("PSEUDO/GRAPHS/Mean_pLDDT_sixteen.png", dpi=200)


##STATS
core_expression= df2[df2["Group"]=="Core"]["Mean_pLDDT"].dropna() #kruskal cant handle
soft_core_expression=df2[df2["Group"]=="Soft-core"]["Mean_pLDDT"].dropna()
shell_expression=df2[df2["Group"]=="Shell"]["Mean_pLDDT"].dropna()
cloud_expression=df2[df2["Group"]=="Cloud"]["Mean_pLDDT"].dropna()

# check normality 

fig, ax = plt.subplots(4, 2, figsize=(12, 16)) 
groups_dict = {
    "Core": core_expression,
    "Soft-core": soft_core_expression,
    "Shell": shell_expression,
    "Cloud": cloud_expression
}
for i, (name, data_group) in enumerate(groups_dict.items()): 
    # Histogram
    ax[i, 0].hist(data_group, bins=50)
    ax[i, 0].set_title(f'{name} - Histogram')
    ax[i, 0].set_xlabel('Gene Expression')
    ax[i, 0].set_ylabel('Frequency')
    
    # Q-Q plot
    stats.probplot(data_group, dist="norm", plot=ax[i, 1]) #q-q plot
    ax[i, 1].set_title(f'{name} - Q-Q Plot')

plt.show()

#Doesnt look normal


h_stat, p_kw = kruskal(core_expression,soft_core_expression,shell_expression, cloud_expression)

if p_kw <0.05:
    print(f"Significant:{p_kw}")
else:
    print(f"Insignificant:{p_kw:15f}")

#calculate the effect size using epsilon squared

n = len(core_expression) + len(soft_core_expression) + len(shell_expression) + len(cloud_expression)
# Formula: E²_R = H / ((n² - 1) / (n + 1))
epsilon_sq = h_stat / ((n**2 - 1) / (n + 1))
print(f"Epsilon squared:{epsilon_sq}")

#post hoc dunn test

dunn = sp.posthoc_dunn(
    df2,
    val_col="Mean_pLDDT",
    group_col="Group",
    p_adjust="holm" 
)
print(f"Dunn:{dunn}")

core_vs_cloud_p = dunn.loc["Core", "Cloud"]
print(f"Core vs Cloud p-value: {core_vs_cloud_p:.15f}")

#medians
print(core_expression.median())
print(soft_core_expression.median())
print(shell_expression.median())
print(cloud_expression.median())


### get mean plddt of rifs and var
print(df2.head(20))
gene_to_plddt=dict(zip(df2["Pangene"], df2["Mean_pLDDT"]))
rif_files=glob.glob("GET_PANGENES_pseudo/rif_analysis/rif_gene_list/*tsv")
var_files=glob.glob("GET_PANGENES_pseudo/Var_analysis/var_gene_list/*tsv")

rif_scores = []
for files in rif_files:
    rif_data = pd.read_csv(files, sep="\t", header=None)
    for gene in rif_data.iloc[:, 0]:
        if gene in gene_to_plddt:
            score = gene_to_plddt[gene]
            if score is not None and not np.isnan(score):
                rif_scores.append(score)

var_scores = []
for files in var_files:
    var_data = pd.read_csv(files, sep="\t", header=None)
    for gene in var_data.iloc[:, 0]:
        if gene in gene_to_plddt:
            score = gene_to_plddt[gene]
            if score is not None and not np.isnan(score):
                var_scores.append(score)

print(f"RIF mean pLDDT: {np.mean(rif_scores)}")
print(f"VAR mean pLDDT: {np.mean(var_scores)}")


product=pd.read_csv("GET_PANGENES_pseudo/peptide_counts_pdb.txt.txt", sep="\t")
product_dict=dict(zip(product["Gene ID"], product["Product Description"]))
df2["Product Description"]=df2["Pangene"].map(product_dict)
lower_quartile = df2["Mean_pLDDT"].quantile(0.25)
low_plddt = df2[df2["Mean_pLDDT"] < lower_quartile]

print(low_plddt["Product Description"].value_counts())
print(low_plddt["Group"].value_counts())
print(len(low_plddt))

unknown = low_plddt[low_plddt["Product Description"].str.contains("unknown function", case=False, na=False)]
print(unknown["Group"].value_counts())