### A script to explore the protein length (aa) of each pangenome occupancy ###
## Includes a normality check and subsequent kurskal waliis and Dunn's post hoc ##
## Input: pangene matrix and protein length data from plasmoDB ##
## Output: grouped box plot showing protein length for the four pangenome occupancies ##

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import numpy as np
from scipy.stats import kruskal
import scikit_posthocs as sp

#read in protein length data
data=pd.read_csv("GET_PANGENES_pseudo/16_protein_length.txt", sep="\t")
#make a dictionary of the gene id and protein length- zip matches
id_to_length = dict(zip(data["Gene ID"], data["Protein Length"]))

print("Number of genes", len(id_to_length))

#read in gene matrix
matrix=pd.read_csv("GET_PANGENES_pseudo/Clusters_renamed_sixteen.tsv", sep="\t", index_col=0)

#make a list of each occupancy and its protein lengths- in a dictionary
occupancy_to_lengths=[]

for col in matrix.columns:
    occupancy = (matrix[col] != "-").sum()
    if occupancy == 16:
        group = "Core"
    elif occupancy == 15:
        group = "Soft-core"
    elif occupancy <= 2:
        group = "Cloud"
    else:
        group = "Shell"
#create a list of the occupancy, group and amino acid count for each gene
    if col in id_to_length:
        occupancy_to_lengths.append({"occupancy":occupancy,
                                                "group":group,
                                                "length":id_to_length[col]})
df=pd.DataFrame(occupancy_to_lengths)

###Statistical analysis

#define groups and data to be compared


core_data=df[df["group"]=="Core"]["length"]
soft_core_data= df[df["group"]=="Soft-core"]["length"]
shell_data=df[df["group"]=="Shell"]["length"]
cloud_data=df[df["group"]=="Cloud"]["length"]

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
fig.savefig("AA_normality.png", dpi=200)


#failed normality so must be kruskal wallis

h_stat, p_kw = kruskal(core_data, soft_core_data, shell_data, cloud_data)
print(f"H-stat:{h_stat}")

if p_kw < 0.05:
    print(f"Significant difference:{p_kw}\n")
else:
    print(f"No significant difference: {p_kw}")

#calculate the effect size (epsilon squared)
n = len(df) 

# Formula: E²_R = H / ((n² - 1) / (n + 1))
epsilon_sq = h_stat / ((n**2 - 1) / (n + 1))
print(f"Epsilon square:{epsilon_sq}")

#if significant-dunn posthoc test

dunn = sp.posthoc_dunn(
    df,
    val_col="length",
    group_col="group",
    p_adjust="holm" #need to adjust as multiple tests
)

print(dunn)

#get the core vs cloud dunn result
core_vs_cloud_p = dunn.loc["Core", "Cloud"]
print(f"Core vs Cloud p-value: {core_vs_cloud_p}")

#check median to see difference between groups
medians=df.groupby("group")["length"].median().sort_values()
print(f"Medians:{medians}")


#make a box plot

colours_dict = {
    "Core": "red",
    "Soft-core": "orange",
    "Shell": "green",
    "Cloud": "blue"
}
fig,ax=plt.subplots(figsize=(12,16))
order=["Cloud", "Shell","Soft-core","Core"]
sns.boxplot(data=df,
               x="group",
               y="length",
               hue="group",
               palette=colours_dict,
               ax=ax,
               order=order,
               legend=False,
               fill=True,
               flierprops={"markerfacecolor":"black"})
# get the max value for positioning the bar
y_max = df["length"].max()
y = y_max * 1.05  
h = y_max * 0.02  

x1, x2 = 0, 3

ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color="black")
ax.text((x1+x2)/2, y+h, "***", ha="center", va="bottom", fontsize=14)


ax.set_ylim(0, y_max * 1.15)

ax.set_xlabel("Pangene Occupancy")
ax.set_ylabel("Amino Acid Count")
legend_elements = [
    Patch(facecolor="red", alpha=0.7, label="Core"),    
    Patch(facecolor="orange", alpha=0.7, label="Soft-core"),
    Patch(facecolor="green", alpha=0.7, label="Shell"),
    Patch(facecolor="blue", alpha=0.7, label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right") 
plt.show()



fig.savefig("aa_box_group_sixteen.png", dpi=300)
