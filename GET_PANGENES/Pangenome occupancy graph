#A python script to produce the pangenome occupancy bar chart, coloured by pangenome classification

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats 
import numpy as np
pangenome = pd.read_csv("GET_PANGENES/GET_PANGENES_growth_output/pangene_matrix.tab", sep="\t", index_col=0)
pangenome = pangenome.drop("chrunsorted", axis=1)   #not data so remove

#handle duplications
pangenome_binary = (pangenome > 0).astype(int)

# Occupancy
occupancy = pangenome_binary.sum(axis=0)  
occupancy_counts = occupancy.value_counts().sort_index() 

print("\nOccupancy counts:")
print(occupancy_counts)

#classify
core_genes=0
soft_core_genes=0
shell_genes=0
cloud_genes=0
for occupancy, total in occupancy_counts.items():
    if occupancy==20:
        core_genes=total
    elif occupancy==19:
        soft_core_genes=total
    elif occupancy in (1,2):
        cloud_genes+=total
    else:
        shell_genes+=total

###Create bar
#colour classification
def classify_colour(x):
    if x == 20:
        return "red"
    elif x == 19:
        return "orange"
    elif x in (1, 2):
        return "blue"
    else:
        return "green"
bar_colours=[classify_colour(x) for x in occupancy_counts.index]
x_ticks=list(range(1,21))
fig,ax=plt.subplots(figsize=(12,6))
bar=ax.bar(occupancy_counts.index, occupancy_counts.values, color=bar_colours)
ax.set_xlabel("Pangene occupancy")
ax.set_ylabel("Number of pangene clusters")
ax.set_xticks(x_ticks)
ax.set_ylim(0,4500)
ax.set_xlim(left=0.5, right=20.5)
ax.bar_label(bar)
legend_elements = [
    Patch(facecolor="red", label="Core"),   
    Patch(facecolor="orange", label="Soft-core"),
    Patch(facecolor="green", label="Shell"),
    Patch(facecolor="blue", label="Cloud"),
]
ax.legend(handles=legend_elements,bbox_to_anchor=(1.14, 1), loc="upper right")
plt.show()

fig.savefig("Pangenome_occupancy_bar_growth.png",dpi=300)


