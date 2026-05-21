### A script to map the paralog counts to the pangenome occupancy ###
## Includes a test of normality, kruskal wallis and Dunn post hoc ##
## Input: pangene matrix and paralog counts for PlasmoDB ##
## Output: boxplot split by occupancy group ##
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats
import seaborn as sns
import numpy as np
from scipy.stats import kruskal
import scikit_posthocs as sp

paralog=pd.read_csv("GET_PANGENES_pseudo/16_paralog_counts.txt", sep="\t")
#only select genes that have a paralog 

paralog_dict = dict(zip(paralog["Gene ID"], paralog["Paralog count"]))

#read in the pangene matrix 
matrix=pd.read_csv("GET_PANGENES_pseudo/Clusters_renamed_sixteen.tsv", sep="\t", index_col=0)


#get dictinary for paralog counts and occupancy
occupancy_to_para=[]
cloud_genes_with_paralog=[]
cloud_genes_no_paralog=[]
core_genes_with_paralog=[]
core_genes_no_paralog=[]

for cluster in matrix.columns:
    occupancy = (matrix[cluster] != "-").sum() 
    if occupancy == 16:
        group = "Core"
    elif occupancy == 15:
        group = "Soft-core"
    elif occupancy in (1, 2):
        group = "Cloud"
    else:
        group = "Shell"
    
    if cluster in paralog_dict:
        paralog_count = paralog_dict[cluster]
        
        if occupancy in (1, 2):
            if paralog_count > 0:
                cloud_genes_with_paralog.append(cluster)
            else:
                cloud_genes_no_paralog.append(cluster)
        elif occupancy == 16:
            if paralog_count > 0:
                core_genes_with_paralog.append(cluster)
            else:
                core_genes_no_paralog.append(cluster)
                
        occupancy_to_para.append({
            "cluster": cluster,
            "occupancy": occupancy,
            "group": group,
            "paralog count": paralog_count
        })
   

df=pd.DataFrame(occupancy_to_para)

core_para_df=df[df["group"]=="Core"]
cloud_para_df=df[df["group"]=="Cloud"]
print(f"Cloud duplications={cloud_para_df['cluster'].duplicated().sum()}\n")
print(f"Core duplications={core_para_df['cluster'].duplicated().sum()}\n")
core_para_df.to_csv("Core_paralog_counts_16.tsv",sep="\t")
cloud_para_df.to_csv("Cloud_paralog_counts_16.tsv",sep="\t")

##Statistical analysis

#define groups and data to be compared

core_data=df[df["group"]=="Core"]["paralog count"]
soft_core_data= df[df["group"]=="Soft-core"]["paralog count"]
shell_data=df[df["group"]=="Shell"]["paralog count"]
cloud_data=df[df["group"]=="Cloud"]["paralog count"]

#check normality
# assess the normality visually as the data is too large for a normality test
fig, ax = plt.subplots(4, 2, figsize=(12, 16))  
groups_dict = {
    "Core": core_data,
    "Soft-core": soft_core_data,
    "Shell": shell_data,
    "Cloud": cloud_data
}
for i, (name, data_group) in enumerate(groups_dict.items()): 
    # Histogram
    ax[i, 0].hist(data_group, bins=50)
    ax[i, 0].set_title(f'{name} - Histogram')
    ax[i, 0].set_xlabel('Paralog Count')
    ax[i, 0].set_ylabel('Frequency')
    
    # Q-Q plot
    stats.probplot(data_group, dist="norm", plot=ax[i, 1]) #q-q plot
    ax[i, 1].set_title(f'{name} - Q-Q Plot')
plt.show()



#failed normality so must be kruskal wallis
h_stat, p_kw = kruskal(core_data,soft_core_data,shell_data, cloud_data)

if p_kw < 0.05:
    print(f"Significant difference:{p_kw}\n")
else:
    print(f"No significant difference: {p_kw}")
n=len(df)
# Formula: E²_R = H / ((n² - 1) / (n + 1))
epsilon_sq = h_stat / ((n**2 - 1) / (n + 1))
print(f"Epsilon square:{epsilon_sq}")

#if significant-dunn posthoc test

dunn = sp.posthoc_dunn(
    df,
    val_col="paralog count",
    group_col="group",
    p_adjust="holm" #need to adjust as multiple tests
)

print(dunn)

#get the core vs cloud dunn result
core_vs_cloud_p = dunn.loc["Core", "Cloud"]
print(f"Core vs Cloud p-value: {core_vs_cloud_p}")

#check median to see difference between groups
medians=df.groupby("group")["paralog count"].median().sort_values()
print(f"Medians:{medians}")


#plot the box
colours_dict = {
    "Core": "red",
    "Soft-core": "orange",
    "Shell": "green",
    "Cloud": "blue"
}
order=["Cloud","Shell","Soft-core","Core"]
fig,ax=plt.subplots(figsize=(12,16))
sns.boxplot(data=df,
               x="group",
               y="paralog count",
               hue="group",
               palette=colours_dict,
               order=order,
               ax=ax,
               legend=False,
             
               flierprops={"markerfacecolor":"black"})

y_max = df["paralog count"].max()
y = y_max * 1.05
h = y_max * 0.02

# cloud is at position 0, core is at position 3
x1, x2 = 0, 3

ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color="black")
ax.text((x1+x2)/2, y+h, "***", ha="center", va="bottom", fontsize=14)


ax.set_ylim(0, y_max * 1.15)
ax.set_xlabel("Pangene Occupancy")
ax.set_ylabel("Paralog Count")
legend_elements = [
    Patch(facecolor="red", alpha=0.7, label="Core"),    
    Patch(facecolor="orange", alpha=0.7, label="Soft-core"),
    Patch(facecolor="green", alpha=0.7, label="Shell"),
    Patch(facecolor="blue", alpha=0.7, label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right") #use bbox to anchor to move the key out
plt.show()


fig.savefig("paralog_box_grouped_16.png", dpi=300)

#save cloud and core as tsv
core_para=pd.DataFrame(core_genes_no_paralog)
cloud_para=pd.DataFrame(cloud_genes_no_paralog)
core_para.to_csv("core_no_para_16", sep="\t")
cloud_para.to_csv("cloud_no_para_16", sep="\t")
