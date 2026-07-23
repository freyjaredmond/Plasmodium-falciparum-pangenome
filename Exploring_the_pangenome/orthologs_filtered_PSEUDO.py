import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats

import seaborn as sns
import numpy as np
from scipy.stats import kruskal
import scikit_posthocs as sp

ortholog=pd.read_csv("PSEUDO/16_ortholog_counts.txt", sep="\t")
#only select genes that have an ortholog

ortholog_dict = dict(zip(ortholog["Gene ID"], ortholog["Ortholog count"]))

#read in the pangene matrix 
matrix=pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)


#get dictinary for ortholog counts and occupancy
occupancy_to_ortho=[]
cloud_genes_with_ortholog=[]
cloud_genes_no_ortholog=[]
core_genes_with_ortholog=[]
core_genes_no_ortholog=[]

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
    if cluster in ortholog_dict: 
        if occupancy in (1,2):
            cloud_genes_with_ortholog.append(cluster)
        elif occupancy==20:
            core_genes_with_ortholog.append(cluster)
        if occupancy in (1,2) and ortholog_dict[cluster]==0:
            cloud_genes_no_ortholog.append(cluster)
        if occupancy== 20 and ortholog_dict[cluster]==0:
            core_genes_no_ortholog.append(cluster)
        occupancy_to_ortho.append({
            "cluster":cluster,
            "occupancy":occupancy,
            "group":group,
            "ortholog count":ortholog_dict[cluster]})    
 

df=pd.DataFrame(occupancy_to_ortho)


#add gene names data
name=pd.read_csv("Clusters_with_gene_names_sixteen.tsv", sep="\t")
combined=df.merge(name, left_on="cluster", right_on="Pangene", how="left")
combined_filtered = combined[~combined["Gene_Name"].isin(["VAR", "RIF","VAR-like"])]

print(combined_filtered.head(30))
#rif genes are not all laballed rif, need to eliminate it if its in the product description
product=pd.read_csv("PSEUDO/product_des.txt", sep="\t")
combined_filtered=combined_filtered.merge(product, left_on="cluster", right_on="Gene ID", how="left")
combined_filtered = combined_filtered[~combined_filtered["Product Description"].str.contains("rif|stevor|var|pfemp1|VAR-like", case=False, na=False)]

#plot the box
colours_dict = {
    "Core": "red",
    "Soft-core": "orange",
    "Shell": "green",
    "Cloud": "blue"
}
fig,ax=plt.subplots(figsize=(12,16))
order=["Cloud","Shell","Soft-core","Core"]
sns.boxplot(data=combined_filtered,
               x="group",
               y="ortholog count",
               hue="group",
               order=order,
               palette=colours_dict,
               ax=ax,
               legend=False,
               flierprops={"markerfacecolor":"black"})
ax.set_xlabel("Pangene Occupancy")
ax.set_ylabel("Ortholog Count")
legend_elements = [
    Patch(facecolor="red", alpha=0.7, label="Core"),    
    Patch(facecolor="orange", alpha=0.7, label="Soft-core"),
    Patch(facecolor="green", alpha=0.7, label="Shell"),
    Patch(facecolor="blue", alpha=0.7, label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right") #use bbox to anchor to move the key out
plt.show()

## the significance was less than 0.001 so need to add a *** connected cloud to core
fig.savefig("PSEUDO/GRAPHS/ortholog_box_grouped_filtered_PSEUDO.png", dpi=300)



sorted_df = combined_filtered.sort_values("ortholog count", ascending=False)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
print(sorted_df.head(20))

##Statistical analysis
#define groups and data to be compared


core_data=combined_filtered[combined_filtered["group"]=="Core"]["ortholog count"]
soft_core_data= combined_filtered[combined_filtered["group"]=="Soft-core"]["ortholog count"]
shell_data=combined_filtered[combined_filtered["group"]=="Shell"]["ortholog count"]
cloud_data=combined_filtered[combined_filtered["group"]=="Cloud"]["ortholog count"]

# assess the normality visually as the data is too large for a normality test
fig, ax = plt.subplots(4, 2, figsize=(12, 16))  # 4 rows and 2 columns (1 for each test type)
groups_dict = {
    "Core": core_data,
    "Soft-core": soft_core_data,
    "Shell": shell_data,
    "Cloud": cloud_data
}
for i, (name, data_group) in enumerate(groups_dict.items()): #create a for loop to do all the plots
    # Histogram
    ax[i, 0].hist(data_group, bins=50)
    ax[i, 0].set_title(f'{name} - Histogram')
    ax[i, 0].set_xlabel('Protein Length')
    ax[i, 0].set_ylabel('Frequency')
    
    # Q-Q plot
    stats.probplot(data_group, dist="norm", plot=ax[i, 1]) #q-q plot
    ax[i, 1].set_title(f'{name} - Q-Q Plot')
plt.show()



#failed normality so must be kruskal wallis
h_stat, p_kw = kruskal(core_data,soft_core_data, shell_data, cloud_data)

if p_kw < 0.05:
    print(f"Significant difference:{p_kw}\n")
else:
    print(f"No significant difference: {p_kw}")
#effect size
n = len(combined_filtered) 

# Formula: E²_R = H / ((n² - 1) / (n + 1))
epsilon_sq = h_stat / ((n**2 - 1) / (n + 1))
print(f"Epsilon square:{epsilon_sq}")

#if significant-dunn posthoc test

dunn = sp.posthoc_dunn(
    combined_filtered,
    val_col="ortholog count",
    group_col="group",
    p_adjust="holm" #need to adjust as multiple tests
)

print(dunn)

#get the core vs cloud dunn result
core_vs_cloud_p = dunn.loc["Core", "Cloud"]
print(f"Core vs Cloud p-value: {core_vs_cloud_p}")

#check median to see difference between groups
medians=combined_filtered.groupby("group")["ortholog count"].median().sort_values()
print(f"Medians:{medians}")
