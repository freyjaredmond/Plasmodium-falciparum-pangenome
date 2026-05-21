### A script to map gene expression taken from PlasmoDB (gene expression data was taken for
## all available RNA-seq data on PlasmoDB v68, excluding the Gambian children dataset ##
## and mapped to the pangenome, with statistical analysis carried out ##
## Input: gene expression data from PlasmoDB, pangenome matrix ##
## Output: boxplot mapping gene expression to each occupancy level ##

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import levene
from scipy.stats import kruskal
import numpy as np
import scikit_posthocs as sp 
from matplotlib.patches import Patch
import seaborn as sns

#import the expression data
expression_data=pd.read_csv("Functional_analysis/Gene_expression_all.txt", sep="\t")
expression_dict = dict(zip(
    expression_data["Gene ID"],  
    expression_data.filter(like="unique").values.tolist())) 
#import gene matrix
matrix=pd.read_csv("GET_PANGENES_pseudo/Clusters_renamed_sixteen.tsv", sep="\t",index_col=0)

#get expression for eacg occupancy
cluster_occupancy_expression=[]
for col in matrix.columns:
    occupancy = (matrix[col] != "-").sum()

    if occupancy == 16:
        group = "Core"
    elif occupancy == 15:
        group = "Soft-core"
    elif occupancy in (1, 2):
        group = "Cloud"
    else:
        group = "Shell"

    gene_3d7 = col if col.startswith("PF3D7") else ""

    if gene_3d7 in expression_dict:
        cluster_occupancy_expression.append({
            "cluster": gene_3d7,
            "occupancy": occupancy,
            "group": group,
            "expression values": expression_dict[gene_3d7]
        })

#make into a data frame
df=pd.DataFrame(cluster_occupancy_expression)
df["mean_expression"] = df["expression values"].apply(np.mean)



#create groups
core_expression= df[df["group"]=="Core"]["mean_expression"]
soft_core_expression=df[df["group"]=="Soft-core"]["mean_expression"]
shell_expression=df[df["group"]=="Shell"]["mean_expression"]
cloud_expression=df[df["group"]=="Cloud"]["mean_expression"]


fig, ax = plt.subplots(4, 2, figsize=(12, 16))  # 4 rows and 2 columns (1 for each test type)
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


#see if evenly distributed using a levene test
levene_stat, p_levene=levene(core_expression, soft_core_expression, shell_expression, cloud_expression)
if p_levene <0.05:
    print(f"Anova unsuitable: {p_levene}")
else:
    print("Anova suitable")

#anova unsuitable so must use kruskal wallis

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
    df,
    val_col="mean_expression",
    group_col="group",
    p_adjust="holm" 
)
print(f"Dunn:{dunn}")

core_vs_cloud_p = dunn.loc["Core", "Cloud"]
print(f"Core vs Cloud p-value: {core_vs_cloud_p:.15f}")

#check the medians
medians=df.groupby("group")["mean_expression"].median().sort_values()
print(f"Medians:{medians}")



#plot the box plot
colours_dict = {
    "Core": "red",
    "Soft-core": "orange",
    "Shell": "green",
    "Cloud": "blue"
}

#log transform for plotting
# log2 transform just for visualisation
df["log2_mean_expression"] = np.log2(df["mean_expression"] + 1)


fig,ax=plt.subplots(figsize=(12,16))
order=["Cloud","Shell","Soft-core","Core"]
sns.boxplot(data=df,
               x="group",
               y="log2_mean_expression",
               palette=colours_dict,
               ax=ax,
               order=order,
               legend=False,
               flierprops={"markerfacecolor":"black"})
y_max = df["log2_mean_expression"].max()
y = y_max * 1.05
h = y_max * 0.02
x1, x2 = 0, 3

ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color="black")
ax.text((x1+x2)/2, y+h, "***", ha="center", va="bottom", fontsize=14)
ax.set_ylim(0, y_max * 1.15)
ax.set_xlabel("Pangene Occupancy")
ax.set_ylabel("Mean expression (log₂(TPM + 1)")
legend_elements = [
    Patch(facecolor="red", alpha=0.7, label="Core"),    
    Patch(facecolor="orange", alpha=0.7, label="Soft-core"),
    Patch(facecolor="green", alpha=0.7, label="Shell"),
    Patch(facecolor="blue", alpha=0.7, label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right") 
plt.show()
fig.savefig("Gene_expression_all_final_sixteen.png", dpi=300)
