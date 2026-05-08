#A python script to identify the number of singleton genes in each genome
#NOTE: Genes with multiple copies in one genome were classified as a singleton
import pandas as pd
import matplotlib.pyplot as plt

pangenome=pd.read_csv("GET_PANGENES/GET_PANGENES_output/pangene_matrix.tab", sep="\t", index_col=0)
pangenome=pangenome.drop("chrunsorted", axis=1)
#decided to class genes as singleton even if there are multiple copies in one genome
pangenome_binary = (pangenome > 0).astype(int)

occupancy=pangenome_binary.sum(axis=0)   
cluster=[]
for key, val in occupancy.items():
    if val==1:
        cluster.append(key)
pangenome_cloud=pangenome_binary[cluster]

cloud_dict={}
for genome in pangenome_cloud.index:
    count = pangenome_cloud.loc[genome].sum()
    cloud_dict[genome]=count

singleton_count=sum(cloud_dict.values())
if singleton_count==2709:
    print("Passed")
else:
    print("Not a match",singleton_count)

clean_names=[]
for name in cloud_dict.keys():
    parts=name.split("Pfalciparum") [1]  #get the number after the species name
    clean_names.append(parts)

##Make barchart
colours = plt.cm.tab20(range(20))  #colour palette
fig,ax=plt.subplots(figsize=(10,15))
ax.barh(range(20),list(cloud_dict.values()),color=colours)  
ax.set_xlabel("Singleton counts", fontsize=20)
ax.set_ylabel("Genome", fontsize=20)
ax.set_yticks(range(20),clean_names)
ax.set_ylim(bottom=-0.5)
plt.tight_layout()

fig.savefig("Singleton.png", dpi=300)
print(cloud_dict)




