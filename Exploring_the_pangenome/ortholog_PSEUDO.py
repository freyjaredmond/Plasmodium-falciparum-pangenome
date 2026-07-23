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
        occupancy_to_ortho.append({
            "cluster":cluster,
            "occupancy":occupancy,
            "group":group,
            "ortholog count":ortholog_dict[cluster]})
        if occupancy in (1,2):
            if ortholog_dict[cluster] > 0:
                cloud_genes_with_ortholog.append(cluster)
            else:
                cloud_genes_no_ortholog.append(cluster)
        elif occupancy == 20:
            if ortholog_dict[cluster] > 0:
                core_genes_with_ortholog.append(cluster)
            else:
                core_genes_no_ortholog.append(cluster)

df=pd.DataFrame(occupancy_to_ortho)


core_ortho_df=df[df["group"]=="Core"]
cloud_ortho_df=df[df["group"]=="Cloud"]
print(f"Cloud duplications={cloud_ortho_df['cluster'].duplicated().sum()}\n")
print(f"Core duplications={core_ortho_df['cluster'].duplicated().sum()}\n")
#core_ortho_df.to_csv("Core_ortholog_counts.tsv",sep="\t")
# cloud_ortho_df.to_csv("Cloud_ortholog_counts.tsv",sep="\t")
##Statistical analysis
#define groups and data to be compared


core_data=df[df["group"]=="Core"]["ortholog count"]
soft_core_data= df[df["group"]=="Soft-core"]["ortholog count"]
shell_data=df[df["group"]=="Shell"]["ortholog count"]
cloud_data=df[df["group"]=="Cloud"]["ortholog count"]

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
n = len(df) 

# Formula: E²_R = H / ((n² - 1) / (n + 1))
epsilon_sq = h_stat / ((n**2 - 1) / (n + 1))
print(f"Epsilon square:{epsilon_sq}")

#if significant-dunn posthoc test

dunn = sp.posthoc_dunn(
    df,
    val_col="ortholog count",
    group_col="group",
    p_adjust="holm" #need to adjust as multiple tests
)

print(dunn)

#get the core vs cloud dunn result
core_vs_cloud_p = dunn.loc["Core", "Cloud"]
print(f"Core vs Cloud p-value: {core_vs_cloud_p}")

#check median to see difference between groups
medians=df.groupby("group")["ortholog count"].median().sort_values()
print(f"Medians:{medians}")


#plot the box
colours_dict = {
    "Core": "red",
    "Soft-core": "orange",
    "Shell": "green",
    "Cloud": "blue"
}
fig,ax=plt.subplots(figsize=(12,16))
order=["Cloud","Shell","Soft-core","Core"]
sns.boxplot(data=df,
               x="group",
               y="ortholog count",
               hue="group",
               order=order,
               palette=colours_dict,
               ax=ax,
               legend=False,
               flierprops={"markerfacecolor":"black"})
# get the max value for positioning the bar
y_max = df["ortholog count"].max()
y = y_max * 1.05
h = y_max * 0.02

# cloud is at position 0, core is at position 3
x1, x2 = 0, 3

ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color="black")
ax.text((x1+x2)/2, y+h, "***", ha="center", va="bottom", fontsize=14)

# extend ylim to make room
ax.set_ylim(0, y_max * 1.15)
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
fig.savefig("PSEUDO/GRAPHS/ortholog_box_grouped_PSEUDO.png", dpi=300)

#save cloud and core as tsv
core_ortholog=pd.DataFrame(pd.Series(core_genes_no_ortholog))
cloud_ortholog=pd.DataFrame(pd.Series(cloud_genes_no_ortholog))
core_ortholog.to_csv("core_no_ortho", sep="\t")
cloud_ortholog.to_csv("cloud_no_ortho", sep="\t")