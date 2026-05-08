# This script plots the genomic position of pangene cluster members across all 14 P. falciparum chromosomes relative to their 3D7 cluster position.
# INPUT: Clusters_renamed.tsv (pangene matrix), GFF files for all 20 genomes
# OUTPUT: Chromosome_location.png — 14 scatter plots, one per chromosome

import pandas as pd
import glob
import re
import matplotlib.pyplot as plt
import seaborn as sns
matrix=pd.read_csv("Clusters_renamed.tsv", sep="\t")
matrix_3d7 = matrix.loc[:, matrix.columns.str.startswith("PF3D7")] #only want cluster that are 3d7

#read in gff files
gff_info_dict={}
gff_files = glob.glob("GET_PANGENES/GET_PANGENES_filtered/inputs_flat/*.gff")

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
genomes = df_filtered["Gene"].str.extract(r'^(P[fF]\w+?)_')[0].unique() #get the genome prefix at the start of all the genes
palette = sns.color_palette("tab20", len(genomes))
colour_map = dict(zip(genomes, palette))  #match the colours to the genomes

fig,ax=plt.subplots(5,3, figsize=(25,40))
ax = ax.flatten()   #so you can loop through all them 
ax[-1].set_visible(False)  #remove the last plot as not needed

for i, chrom in enumerate(all_chroms):
    current_ax = ax[i] 
    for genome in genomes:
        chrom_genome=chrom[chrom["Gene"].str.startswith(str(genome))] #get the genome values for that chromosome
        current_ax.scatter(chrom_genome["Cluster_location"], chrom_genome["Start_position"], color=colour_map[genome], label=genome,s=1.5)
    current_ax.set_xlabel("3D7 Position", fontsize=7)
    current_ax.set_ylabel("Genome Position", fontsize=7)
    current_ax.set_title(f"Chromosome{i+1}", fontsize=7)#account for indexing
    current_ax.tick_params(axis="x", labelsize=7)
    current_ax.tick_params(axis="y", labelsize=7)
    current_ax.ticklabel_format(style="plain", axis="both") #remove the scientific notation from the axis
ax[0].set_xticks([0,100000,200000,300000,400000,500000,600000,700000])
ax[0].set_yticks([0,100000,200000,300000,400000,500000,600000,700000])
ax[1].set_xticks([0,200000,400000,600000,800000,1000000,1200000])
ax[1].set_yticks([0,200000,400000,600000,800000,1000000,1200000])
ax[2].set_xticks([0,200000,400000,600000,800000,1000000,1200000])
ax[2].set_yticks([0,200000,400000,600000,800000,1000000,1200000])
ax[3].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000])
ax[3].set_yticks([0,200000,400000,600000,800000,1000000,1200000,1400000])
ax[4].set_yticks([0,200000,400000,600000,800000,1000000,1200000,1400000])
ax[4].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000])
ax[5].set_yticks([0,200000,400000,600000,800000,1000000,1200000,1400000])
ax[5].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000])
ax[6].set_yticks([0,400000,800000,1200000,1600000,2000000,2400000])
ax[6].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])
ax[7].set_yticks([0,200000,400000,600000,800000,1000000,1200000,1400000,160000])
ax[7].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])
ax[8].set_yticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])
ax[8].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])
ax[9].set_yticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])
ax[9].set_xticks([0,200000,400000,600000,800000,1000000,1200000,1400000,1600000])
ax[10].set_yticks([0,400000,800000,1200000,1600000,2000000,2400000])
ax[10].set_xticks([0,400000,800000,1200000,1600000,2000000,2400000])
ax[11].set_yticks([0,400000,800000,1200000,1600000,2000000,2400000])
ax[11].set_xticks([0,400000,800000,1200000,1600000,2000000,2400000])
ax[12].set_yticks([0,400000,800000,1200000,1600000,2000000,2400000,2800000])
ax[12].set_xticks([0,400000,800000,1200000,1600000,2000000,2400000,2800000])
ax[13].set_yticks([0,500000,1000000,1500000,2000000,2500000,3000000,3500000])
ax[13].set_xticks([0,500000,1000000,1500000,2000000,2500000,3000000,3500000])
plt.subplots_adjust(hspace=1.0, wspace=0.4)  #seperate the plots to make them readable

  
handles, labels = ax[0].get_legend_handles_labels()  #get the first subplots legends
legend_dict = dict(zip(labels, handles)) #get labels and there corresponding colours
fig.legend(legend_dict.values(), legend_dict.keys(), 
           loc="lower right", fontsize=9, 
           bbox_to_anchor=(1.0, 0.1))


plt.show()
fig.savefig("Chromosome_location.png", dpi=300)

