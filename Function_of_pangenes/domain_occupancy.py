### A script to match interpro ids to each cluster and find the representative domain for that cluster##
## The occupancy of that representative domain for that cluster is then calculated ##
## The mean occupacncy of that domain is then calculated across the pangenome ##
## This script is identifies the occupancy of selected genes ##
## Input: pangene matrix and interpro ids for each cluster from PlasmoDB ##
## Output: representative domain, occupancy and status, boxplot of occupancy of selected domains ##

import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import seaborn as sns

matrix=pd.read_csv("GET_PANGENES_pseudo/Clusters_renamed_sixteen.tsv", sep="\t")
interpro=pd.read_csv("Functional_analysis/ID_to_gene.txt.txt", sep="\t")
interpro_dict=dict(zip(interpro["Gene ID"], interpro["Interpro ID"]))
interpro_desc_dict = {}
for ids, desc in zip(interpro["Interpro ID"], interpro["Interpro Description"]): #match interpro id to description
    if ";" in str(ids): #split for multiple ids
        for id, d in zip(ids.split(";"), desc.split(";")): #match each id to its description
            interpro_desc_dict[id] = d
    else:
        interpro_desc_dict[ids] = desc


data_table=[]
gene_table=[]
random.seed(42)
for col in matrix.columns:
    cluster_interpro=[]
    for gene in matrix[col]:
        if gene != "-" and gene in interpro_dict: 
            interpro_ids=interpro_dict[gene]
            if pd.isna(interpro_ids):  # skip genes with no interpro 
                continue

            gene_interpros=[]
            if ";" in str(interpro_ids):
                for interpro_id in interpro_ids.split(";"):
                    cluster_interpro.append(interpro_id)
                    gene_interpros.append(interpro_id)
            else:
                cluster_interpro.append(interpro_ids)
                gene_interpros.append(interpro_ids)

            gene_table.append({
                "Cluster": col,
                "Gene":gene,
                "Interpro_IDs": gene_interpros,
            })
    if cluster_interpro and len(cluster_interpro) > 0:
        counts = pd.Series(cluster_interpro).value_counts() #cant do value counts on a list
        max_count = counts.max()
        top_domains = counts[counts == max_count].index.tolist() #gets the domain with that value
        representative_domain = random.choice(top_domains) #selects a random one
        counter=0
        for val in cluster_interpro:
            if val==representative_domain:
                counter+=1
        

        data_table.append({"Cluster":col,
                       "Representative Domain":representative_domain,
                       "Representative Function":interpro_desc_dict[representative_domain],
                      "Occupancy":counter})
gene_df=pd.DataFrame(gene_table)
df=pd.DataFrame(data_table)
    
print(gene_df.head())
print(df.head())

df.to_csv("Representative_domains_sixteen.tsv", sep="\t")

#get mean domain occupancy
mean_domain=df.groupby("Representative Domain")["Occupancy"].mean().round(0).astype(int).reset_index() #get the mean for each domain
mean_domain.columns = ["Representative Domain", "Mean Occupancy"]
mean_domain_df=df.merge(mean_domain, on="Representative Domain", how="left")
print(mean_domain_df.head())
mean_domain_df.to_csv("GET_PANGENES_pseudo/Representative_domains_sixteen.tsv", sep="\t")

filtered_mean_domain_df=mean_domain_df[mean_domain_df["Mean Occupancy"]>=5]

#classify mean domain occupancy

conditions = [
    filtered_mean_domain_df["Mean Occupancy"] < 10,
    (filtered_mean_domain_df["Mean Occupancy"] >= 10) & (filtered_mean_domain_df["Mean Occupancy"] <15),
    filtered_mean_domain_df["Mean Occupancy"] >15
]

choices = ["Highly Variable", "Partially Variable", "Invariable"]

filtered_mean_domain_df["Classification"] = np.select(conditions, choices, default="Unknown") #selects the choice based off the conditions you set

filtered_mean_domain_df.to_csv("GET_PANGENES_pseudo/Representative_domains_classified.tsv", sep="\t")

value_counts=filtered_mean_domain_df.value_counts("Representative Domain")
print(value_counts.head(20))
value_counts_desc=mean_domain_df.value_counts("Representative Function")
print(value_counts_desc.head(60)) #most commonly reported domains

#get the five
six=("P-loop containing nucleoside triphosphate hydrolase", "Protein kinase-like domain superfamily","RNA-binding domain superfamily","Plasmodium RESA, N-terminal","Exported protein, PHISTa/b/c, conserved domain, Plasmodium","Schizont-infected cell agglutination, C-terminal domain")
#get top 5 id rows
top_five = filtered_mean_domain_df[filtered_mean_domain_df["Representative Function"].isin(six)]

fig,ax=plt.subplots(figsize=(14,6))
sns.boxplot(data=top_five,
             x="Representative Function",
             y="Occupancy",
             ax=ax,
             order=six,
             palette="pastel",
             flierprops={"markerfacecolor":"black"})

ax.set_xlabel("InterPro Term")
ax.set_ylabel("Domain Occupancy")
plt.subplots_adjust(bottom=0.4)

ax.axvspan(-0.5, 2.5, alpha=0.1, color='steelblue', label='Core')
ax.axvspan(2.5, 5.5, alpha=0.1, color='salmon', label='Host-Interaction')

ax.text(1, ax.get_ylim()[1] * 1.1, 'Core', 
        ha='center', va='top', fontsize=11) #plot text above box 2, 1.1 x the y limit
ax.text(4, ax.get_ylim()[1] * 1.1, 'Host-Interaction', 
        ha='center', va='top', fontsize=11)
ax.margins(x=0)

new_labels = [
    "P-loop NTPase",
    "Protein kinase-like domain",
    "RNA-binding domain",
    "Plasmodium RESA",
    "Exported protein, PHISTa/b/c",
    "Schizont-infected cell agglutination"
]

ax.set_xticklabels(new_labels, rotation=45, ha='right')
plt.show()
fig.savefig("GET_PANGENES_pseudo/Domain_occupancy_families_six_sixteen.png", dpi=300)
