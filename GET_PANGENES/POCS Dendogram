# A python script to create a POCS heatmap and dendogram using complete linkage hierarchical clustering to Euclidean distances calculated between genome assemblies
# INPUT: POCS matrix.tab from GET_PANGENES
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# Data input
pocs=pd.read_csv("GET_PANGENES/GET_PANGENES_growth_output/POCS.matrix.tab", sep="\t", index_col=0)
pocs.index=pocs.index.str.replace("PlasmoDB-68_Pfalciparum","") #must say that its a str
pocs.columns=pocs.columns.str.replace("PlasmoDB-68_Pfalciparum","")


#create dendrogram
g=sns.clustermap(pocs, cmap="magma", figsize=(13,14), annot=True, fmt=".0f", annot_kws={'size': 15})
fig=g.fig
ax=g.ax_heatmap
cbar=g.ax_cbar
cbar.set_xlabel("POCS")
ax.tick_params(axis='both', labelsize=15)




fig.savefig("POCS_heatmap.png", dpi=300)
