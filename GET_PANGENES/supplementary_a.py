import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
import io
from PIL import Image
import seaborn as sns
fig = plt.figure(figsize=(12,18))
gs = gridspec.GridSpec(2, 2, figure=fig,
                       width_ratios=[1, 1], hspace=0.4, wspace=0.3)
ax_a = fig.add_subplot(gs[0, 0])   # POCS spans all rows on left
ax_b = fig.add_subplot(gs[0, 1])   # singleton top right
ax_c = fig.add_subplot(gs[1, 0])   # soft-core middle right
ax_d = fig.add_subplot(gs[1, 1])   # scatter bottom right
#####
colour_pallette={"3D7":"firebrick",
                 "7G8-2019":"slategrey",
                 "7G8":"slategrey",
                 "CD01":"slategrey",
                 "DD2":"slategrey",
                 "HB3":"slategrey",
                 "IT":"slategrey",
                 "GA01":"slategrey",
                 "GB4":"slategrey",
                 "GN01":"slategrey",
                 "KE01":"slategrey",
                 "KH01":"slategrey",
                 "KH02":"slategrey",
                 "ML01":"orange",
                 "NF135C10":"orange",
                 "NF166":"slategrey",
                 "NF54":"slategrey",
                 "TG01":"orange",
                 "SD01":"orange",
                 "SN01":"slategrey"}

colour_pallette2={"3D7":"firebrick",
                 "7G8-2019":"coral",
                 "7G8":"sienna",
                 "CD01":"gold",
                 "DD2":"yellowgreen",
                 "HB3":"palegreen",
                 "IT":"slategrey",
                 "GA01":"lightseagreen",
                 "GB4":"khaki",
                 "GN01":"steelblue",
                 "KE01":"midnightblue",
                 "KH01":"blueviolet",
                 "KH02":"plum",
                 "ML01":"deeppink",
                 "NF135C10":"brown",
                 "NF166":"black",
                 "NF54":"olive",
                 "TG01":"crimson",
                 "SD01":"orange",
                 "SN01":"darkgreen"}
### POCS 20
pocs=pd.read_csv("GET_PANGENES_growth_output/POCS.matrix.tab", sep="\t", index_col=0)
pocs.index=pocs.index.str.replace("PlasmoDB-68_Pfalciparum","") #must say that its a str
pocs.columns=pocs.columns.str.replace("PlasmoDB-68_Pfalciparum","")

#create denogram
g = sns.clustermap(pocs, cmap="magma", figsize=(20,20), annot=True, fmt=".0f", annot_kws={'size': 25},dendrogram_ratio=0.3)
for collection in g.ax_row_dendrogram.collections:
    collection.set_linewidth(3)
for collection in g.ax_col_dendrogram.collections:
    collection.set_linewidth(3)
cluster_fig = g.fig
g.ax_heatmap.set_ylabel("")
plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90, ha='right', fontsize=35)
plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0, fontsize=35)
g.ax_cbar.tick_params(labelsize=40)

buf = io.BytesIO()
cluster_fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
plt.close(cluster_fig)
buf.seek(0)
ax_a.imshow(Image.open(buf))
ax_a.axis("off")

### singleton bar

import pandas as pd
import matplotlib.pyplot as plt

pangenome=pd.read_csv("GET_PANGENES_growth_output/pangene_matrix.tab", sep="\t", index_col=0)
pangenome=pangenome.drop("chrunsorted", axis=1)
#going to class genes as singleton even if there are multiple copies in one single genome
pangenome_binary = (pangenome > 0).astype(int)

occupancy=pangenome_binary.sum(axis=0)   #axis is what you collapse (rows=0, col=1)
cluster=[]
for key, val in occupancy.items():
    if val==1:
        cluster.append(key)
pangenome_cloud=pangenome_binary[cluster]

cloud_dict={}
for genome in pangenome_cloud.index:
    clean_genome = genome.replace("Dd2", "DD2")
    count = pangenome_cloud.loc[genome].sum()
    cloud_dict[clean_genome] = count
### cloud_dict = pangenome_cloud.sum(axis=1).to_dict()-- better way
#sanity check-sum of singletons should be 2709 (occupancy=1)
singleton_count=sum(cloud_dict.values())
if singleton_count==2709:
    print("Passed")
else:
    print("Not a match",singleton_count)
cloud_dict = dict(sorted(cloud_dict.items(), key=lambda x: x[1], reverse=True))

clean_names = []
for name in cloud_dict.keys():
    parts = name.split("Pfalciparum")[1]
    clean_names.append(parts)

bar_colours = [colour_pallette.get(name, "gray") for name in clean_names]
clean_names=[]
for name in cloud_dict.keys():
    parts=name.split("Pfalciparum") [1]  #get the number after the species name
    clean_names.append(parts)

##Make barchart

bar_colours = [colour_pallette.get(name, "gray") for name in clean_names]
ax_b.barh(range(20),list(cloud_dict.values()),color=bar_colours)  #horizontal bar, has spacing and y values first #list keeps in the correct order to match names
ax_b.set_xlabel("Singleton counts", fontsize=10)
ax_b.set_ylabel("Genome", fontsize=10)
ax_b.set_yticks(range(20),clean_names, fontsize=8)
ax_b.set_ylim(bottom=-0.5)
ax_b.axvline(x=135, color='black', linestyle='--', linewidth=1.5, label='Equal Distribution = 135')
ax_b.legend(fontsize=12)

## Plot soft core

matrix = pd.read_csv("Clusters_renamed.tsv", sep="\t")
matrix = matrix.set_index(matrix.columns[1])
print(matrix.index[:5].tolist())
print(matrix.head())
print(matrix.columns[:10].tolist())
soft_core_absent = []
for col in matrix.columns:
    if col.startswith("source"):
        continue
    occupancy = (matrix[col] != "-").sum()
    if occupancy == 19:
        absent_genomes = matrix.index[matrix[col] == "-"].tolist()
        for genome in absent_genomes:
            soft_core_absent.append({
                "cluster": col,
                "absent_genome": genome.replace("PlasmoDB-68_Pfalciparum", "")
            })


soft_core_df = pd.DataFrame(soft_core_absent)
soft_core_df["absent_genome"] = soft_core_df["absent_genome"].str.replace("Dd2", "DD2")

print(len(soft_core_df))


vc = soft_core_df["absent_genome"].value_counts().reset_index()
vc.columns = ["Genome", "Count"]
bar_colours_c = [colour_pallette.get(name, "gray") for name in vc["Genome"]]
ax_c.barh(range(len(vc)), vc["Count"], color=bar_colours_c)
ax_c.set_yticks(range(len(vc)), vc["Genome"], fontsize=8)
ax_c.set_xlabel("Count", fontsize=10)
ax_c.set_ylabel("Genome", fontsize=10)
ax_c.axvline(x=32, color='black', linestyle='--', linewidth=1.5, label='Equal Distribution = 32')
ax_c.legend(fontsize=12)

### sd01 discepancy

import pandas as pd
import glob
import re
import matplotlib.pyplot as plt
import seaborn as sns
matrix=pd.read_csv("Clusters_renamed.tsv", sep="\t")
matrix_3d7 = matrix.loc[:, matrix.columns.str.startswith("PF3D7")] #only want cluster that are 3d7

#read in gff files
gff_info_dict={}
gff_files = glob.glob("GET_PANGENES_filtered/inputs_flat/*gff")

for gff in gff_files:
    with open(gff, "r") as f:
        for lines in f:
            if lines.startswith("#"):
                continue
            parts=lines.split("\t")
            if parts[2]=="gene":
                id=parts[8]
                gene_id=id.split(";")[0].replace("ID=","")
                start=parts[3]    #re.sub replaces
                chromosome = re.sub(r"_v\d+$", "", parts[0]) #remove the _v3 at the end of 3d7 (matches v and one or more digits at the end of string)
                gff_info_dict[gene_id]=chromosome,start


#skip chromosomes that are API etc
def get_chromosome(chrom_string):
    match = re.search(r'_(\d{2})$', chrom_string) #get the chromosome number catches 2 digits at the end of the string
    if match:
        number = int(match.group(1))
        if 1 <= number <= 14:  #only 14 chromosomes
            return number
    return None 
data_for_table=[]
for cols in matrix_3d7.columns:
    col=cols.split(",")[0]
    info_cluster=gff_info_dict[col]
    chromosome_string_cluster=info_cluster[0]
    chromosome_cluster=get_chromosome(chromosome_string_cluster) #use chromosome formula
    start_3d7=info_cluster[1]
    for genes in matrix_3d7[cols]:
        gene=genes.split(",")[0]
        if gene!="-":
            info=gff_info_dict[gene]
            chromosome_string=info[0]
            chromosome=get_chromosome(chromosome_string)
            if chromosome is None:  
                continue
            start=info[1]
            data_for_table.append({"Cluster_chromosome":chromosome_cluster,
                                   "Cluster_location":start_3d7,
                                   "Cluster":col,
                                   "Gene": gene,
                                   "Chromosome":chromosome,
                                   "Start_position":start})

df=pd.DataFrame(data_for_table)
df["Start_position"] = df["Start_position"].astype(int)
df["Cluster_location"] = df["Cluster_location"].astype(int)


#remove genes that arent in the same chromosome as the cluster identifier
df_filtered=df[df["Chromosome"]==df["Cluster_chromosome"]]

print(df_filtered.head(20))

chrom1 = df_filtered[df_filtered["Cluster_chromosome"] == 1]
chrom2 = df_filtered[df_filtered["Cluster_chromosome"] == 2]
chrom3 = df_filtered[df_filtered["Cluster_chromosome"] == 3]
chrom4 = df_filtered[df_filtered["Cluster_chromosome"] == 4]
chrom5 = df_filtered[df_filtered["Cluster_chromosome"] == 5]
chrom6 = df_filtered[df_filtered["Cluster_chromosome"] == 6]
chrom7 = df_filtered[df_filtered["Cluster_chromosome"] == 7]
chrom8 = df_filtered[df_filtered["Cluster_chromosome"] == 8]
chrom9 = df_filtered[df_filtered["Cluster_chromosome"] == 9]
chrom10 = df_filtered[df_filtered["Cluster_chromosome"] == 10]
chrom11 = df_filtered[df_filtered["Cluster_chromosome"] == 11]
chrom12 = df_filtered[df_filtered["Cluster_chromosome"] == 12]
chrom13 = df_filtered[df_filtered["Cluster_chromosome"] == 13]
chrom14 = df_filtered[df_filtered["Cluster_chromosome"] == 14]

print(chrom1.head(20))

#plot
all_chroms=[chrom1,chrom2,chrom3,chrom4,chrom5,chrom6,chrom7,chrom8,chrom9,chrom10,chrom11,chrom12,chrom13,chrom14]

#match colours
genomes = df_filtered["Gene"].str.extract(r'^(P[fF]\w+?)_')[0].replace("Dd2","DD2").unique() #get the genome prefix at the start of all the genes

for genome in genomes:
    clean_genome = genome.replace("Pf", "").replace("PF", "")
    chrom_genome = chrom7[chrom7["Gene"].str.startswith(str(genome))]
    ax_d.scatter(chrom_genome["Cluster_location"], chrom_genome["Start_position"], 
                 color=colour_pallette2.get(clean_genome, "gray"), label=clean_genome, s=1.5)
ax_d.set_xlabel("3D7 Position", fontsize=10)
ax_d.set_ylabel("Genome Position", fontsize=10)
ax_d.tick_params(axis="x", labelsize=7)
ax_d.tick_params(axis="y", labelsize=7)
ax_d.ticklabel_format(style="plain", axis="both") 

ax_d.set_yticks([0,400000,800000,1200000,1600000,2000000,2400000])
ax_d.set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])


  
handles, labels = ax_d.get_legend_handles_labels()  #get the first subplots legends
legend_dict = dict(zip(labels, handles)) #get labels and there corresponding colours
fig.legend(legend_dict.values(), legend_dict.keys(), 
           loc="lower right", fontsize=9, 
           bbox_to_anchor=(1.0, 0.1), markerscale=5)


ax_a.text(-0.01, 1.01, 'A', transform=ax_a.transAxes, fontsize=14, fontweight='bold', va='bottom', ha='right')
ax_b.text(-0.01, 1.01, 'B', transform=ax_b.transAxes, fontsize=14, fontweight='bold', va='bottom', ha='right')
ax_c.text(-0.01, 1.01, 'C', transform=ax_c.transAxes, fontsize=14, fontweight='bold', va='bottom', ha='right')
ax_d.text(-0.01, 1.01, 'D', transform=ax_d.transAxes, fontsize=14, fontweight='bold', va='bottom', ha='right')
fig.savefig("panels/Supplementary_a.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()


