# This script reads the GET_PANGENES quality control output and produces histograms
# of the following metrics across all pangene clusters:
# - SE of protein length (SE_len)
# - SE of sequence distance (SE_dist)  
# - MSA completeness (Ca)
# - Maximum distance in protein alignment (max_dist)
# INPUT: all_clusters_quality.txt (output from check_quality.pl)
# OUTPUT: SE_length.png, SE_distance.png, Ca.png, Max_distance.png

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
#have to rename the columns
df = pd.read_csv("GET_PANGENES/Quality/all_clusters_quality.txt", sep="\t", header=None,
                 names=["file", "1stisof", "occup", "seqs", "mode_len", "SE_len",
                        "mode_exons", "SE_exons", "mode_dist", "max_dist", "SE_dist",
                        "sites", "Ca", "Cr_max", "Cr_min", "Cc_max", "Cc_min", "Cij_max", "Cij_min"])
#drop warning lines
df = df[df["file"].str.endswith(".fna")]

#se length

fig,ax=plt.subplots(figsize=(6,10))
p=sns.histplot(data=df,
              x="SE_len",bins=20,ax=ax,color="green")
ax.set_xlabel("SE length")
plt.show()
fig.savefig("GET_PANGENES/Quality/SE_length.png", dpi=300)

#SE distance

fig,ax=plt.subplots(figsize=(6,10))
p=sns.histplot(data=df,
              x="SE_dist",bins=20,ax=ax,color="green")
ax.set_xlabel("SE Distance")
plt.show()
fig.savefig("GET_PANGENES/Quality/SE_distance.png", dpi=300)

#Ca-MSA completeness
fig,ax=plt.subplots(figsize=(6,10))
p=sns.histplot(data=df,
              x="Ca",bins=20,ax=ax,color="green")
ax.set_xlabel("MSA Completeness")
plt.show()
fig.savefig("GET_PANGENES/Quality/Ca.png", dpi=300)

#max distance
fig,ax=plt.subplots(figsize=(6,10))
p=sns.histplot(data=df,
              x="max_dist",bins=20,ax=ax,color="green")
ax.set_xlabel("Max distance in protein alignment")
plt.show()
fig.savefig("GET_PANGENES/Quality/Max_distance.png", dpi=300)
