### A script to identify the percentage of pangenes that have at least 2 peptides and to produce a boxplot ###
## Chi2 test was also carried out to compare core vs cloud ##
## Input: peptide data was taken from https://doi.org/10.1093/gigascience/giac008, pangene matrix ##
## Output: bar chart with the percemtage of pangenes that had >2 peptides in this proteomics study ##
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import chi2_contingency
from scipy.stats import kruskal
from scipy.stats import wilcoxon
import numpy as np
import scikit_posthocs as sp 
from matplotlib.patches import Patch
import seaborn as sns

#import the expression data
expression_data=pd.read_csv("Functional_analysis/Siddiqui/Peptide_count.csv", sep=",")
expression_data_filered=expression_data[expression_data["Organism"]=="P. falciparum"]
expression_dict=dict(zip(expression_data_filered["BGSInferenceId"], expression_data_filered["Unique peptides"]))

#import gene matrix
matrix=pd.read_csv("GET_PANGENES_pseudo/Clusters_renamed_sixteen.tsv", sep="\t",index_col=0)
#rename the cluster to 3D7
cluster_occupancy_peptide=[]
cluster_occupancy_total=[]
for col in matrix.columns:
    occupancy = (matrix[col] != "-").sum()

    if occupancy == 16:
        group = "core"
    elif occupancy == 15:
        group = "soft-core"
    elif occupancy in (1, 2):
        group = "cloud"
    else:
        group = "shell"

    cluster_occupancy_total.append({"cluster": col,
                                    "occupancy": occupancy,
                                    "group": group})

    if col in expression_dict:
        if expression_dict[col] >= 2:
            cluster_occupancy_peptide.append({"cluster": col,
                                              "occupancy": occupancy,
                                              "group": group,
                                              "peptide count": expression_dict[col]})



#make into a data frame
peptide_df=pd.DataFrame(cluster_occupancy_peptide)
total_df=pd.DataFrame (cluster_occupancy_total)

#get the percentage for each occupancy for plotting
total_per_occupancy=total_df.groupby("occupancy")["cluster"].count()
print(f"Total clusters:{total_per_occupancy}\n")
peptide_per_occupancy=peptide_df.groupby("occupancy")["cluster"].count().reindex(total_per_occupancy.index, fill_value=0) #make same length
print(f"Peptide per occupancy: {peptide_per_occupancy}")
percentage_per_occupancy=(peptide_per_occupancy)/(total_per_occupancy)*100
print(percentage_per_occupancy)

#create the data frame for plotting
occupancy_to_group = total_df.drop_duplicates("occupancy").set_index("occupancy")["group"] #make a look up table
percentage_df = pd.DataFrame({
    "occupancy": total_per_occupancy.index,
    "percentage": percentage_per_occupancy.values,
    "group": occupancy_to_group.reindex(total_per_occupancy.index).values #add group labels, make sure they align by reindexing
}).sort_values("occupancy") #sort by occupancy
#get the percentage for each group for stats

total_per_group=total_df.groupby("group")["cluster"].count()
peptide_per_group=peptide_df.groupby("group")["cluster"].count()
percentage_per_group=(peptide_per_group)/(total_per_group)*100
print(percentage_per_group)
percentage_group_df = pd.DataFrame({
    "group": percentage_per_group.index,
    "percentage": percentage_per_group.values
})
#chi2 to compare between cloud and core 
detected=peptide_per_group.reindex(total_per_group.index, fill_value=0) #make them the same length
not_detected=total_per_group-detected
#build contigency table
contigency_table=pd.DataFrame({"Detected":detected,
                               "Undetected":not_detected})

#extract core and cloud
contingency_table_filtered=contigency_table.loc[["core", "cloud"]]
chi2, p, dof, expected = chi2_contingency(contingency_table_filtered)
print(f"Chi2:{chi2}\n")
print(f"P-value:{p}\n")

#run an effect size calculation (cramers)
n = contingency_table_filtered.values.sum()  
min_dim = min(contingency_table_filtered.shape) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))
print(f"Cramers v:{cramers_v}\n")

#plot the box
colours_dict = {
    "core": "red",
    "soft-core": "orange",
    "shell": "green",
    "cloud": "blue"
}
order=["cloud","shell","soft-core","core"]
fig,ax=plt.subplots(figsize=(12,16))
sns.barplot(data=percentage_group_df,
               x="group",
               y="percentage",
               hue="group",
               palette=colours_dict,
               ax=ax,
               legend=False,
            errorbar=None,
            order=order)

y_max = percentage_group_df["percentage"].max()
y = y_max * 1.05
h = y_max * 0.02
x1, x2 = 0, 3

ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color="black")
ax.text((x1+x2)/2, y+h, "***", ha="center", va="bottom", fontsize=14)
ax.set_ylim(0, y_max * 1.15)
ax.set_xlabel("Pangene Occupancy")
ax.set_ylabel("Percentage of pangenes with peptide count ≥ 2")
legend_elements = [
    Patch(facecolor="red", alpha=0.7, label="Core"),    
    Patch(facecolor="orange", alpha=0.7, label="Soft-core"),
    Patch(facecolor="green", alpha=0.7, label="Shell"),
    Patch(facecolor="blue", alpha=0.7, label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right") 
plt.show()
fig.savefig("Functional_analysis/peptide_sixteen.png", dpi=300)
    
