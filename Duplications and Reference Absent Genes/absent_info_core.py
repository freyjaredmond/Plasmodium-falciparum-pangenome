import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
#read in the absent genes and the bed files
data = pd.read_csv("PSEUDO/no_flank_unmapped_genes.tsv", sep="\t")
bed_files = glob.glob("GET_PANGENES_pseudo/Core_coords/Core_coords_fixed/*.bed")

# load all bed files into a dictionary of dataframes
bed_dict = {}
for bed_file in bed_files:
    bed_name = os.path.basename(bed_file)
    bed_genome = bed_name.split("_core")[0]
    bed_df = pd.read_csv(bed_file, sep="\t", header=None,
                         names=["chrom", "start", "end", "name"]) #add headers
    bed_dict[bed_genome] = bed_df

#allocate genes into core or variable groups based off location
location_data = []
for idx, row in data.iterrows():
    gene = row["Gene ID"]
    genome = row["Genome"]
    chromosome = row["Chromosome"]
    start = int(row["Start Position"])
    end = int(row["End Position"])

    label = "No BED found"

    if genome in bed_dict:
        bed_df = bed_dict[genome]
        chr_bed = bed_df[bed_df["chrom"] == chromosome]

        if len(chr_bed) == 0:
            label = "Subtelomeric/Variable" #contig was not part of the core
        else:
            core_regions = chr_bed[chr_bed["name"].str.startswith("Core")] #core region
            var_regions = chr_bed[chr_bed["name"].str.startswith("Var")] #variable regions within core

            in_core = core_regions[
                (core_regions["start"] <= start) & (core_regions["end"] >= end) #in core if the start of the core is earlier than the start of the gene, and the end of the core is greater than the end of the gene
            ]
            in_var = var_regions[
                (var_regions["start"] <= start) & (var_regions["end"] >= end) #same for the variable
            ]

            if len(in_core) > 0:
                if len(in_var) > 0:
                    label = "Subtelomeric/Variable"   #variable region contained within the core
                else:
                    label = "Core"
            else:
                label = "Subtelomeric/Variable" #not in the core

    location_data.append({"Gene ID": gene, "Location": label})

location_df = pd.DataFrame(location_data)
final_df = data.merge(location_df, on="Gene ID", how="left")

final_df = final_df.drop(columns=["Unnamed: 0", "Genes unmapped"])
final_df["Genes in cluster"] = final_df["Genes in cluster"].str.strip("[]").str.replace("'", "")

final_df.to_csv("PSEUDO/no_flank_unmapped_genes_location.csv", sep="\t", index=False)
print(final_df["Location"].value_counts())

## filter by the location type
core_df=final_df[final_df["Location"]=="Core"]
core_df.to_csv("PSEUDO/no_flank_core_unmapped_genes.csv",sep=",", index=False)
print("********************")
print(f"The number of core:{len(core_df)}")
print(len(core_df["Cluster"].value_counts()))

print(core_df["Product Description"].value_counts())

### core not singletons
core_df_shell=core_df[core_df["Occupancy"]>1]
print(f"Core no singleton:{len(core_df_shell)}")
core_df_shell.to_csv("PSEUDO/core_excluding_singletons.csv", sep=",", index=False)

#core no singletons consistency
core_df_shell_100=core_df_shell[core_df_shell["Percentage of genes unmapped"]==100]
print(f"Core no singleton 100%:{len(core_df_shell_100)}")
core_df_shell_100.to_csv("PSEUDO/core_excluding_singletons_100%.csv", sep=",", index=False)

vc=core_df_shell["Product Description"].value_counts()

import textwrap

wrapped_labels = [textwrap.fill(label, width=30) for label in vc.index]

fig, ax = plt.subplots(figsize=(20, 8))  # much wider figure
ax.bar(range(len(vc)), vc.values, color="darkgreen")
ax.set_xlabel("Description")
ax.set_ylabel("Count")
ax.set_xticks(range(len(vc)))
ax.set_xticklabels(wrapped_labels, rotation=45, ha="right", fontsize=7)
plt.subplots_adjust(bottom=0.4, left=0.1)

plt.show()
fig.savefig("PSEUDO/Graphs/no_flank_core_description.png", dpi=300, bbox_inches="tight")


## filter by the location type
var_df=final_df[final_df["Location"]=="Subtelomeric/Variable"]
print(len(var_df["Cluster"].value_counts()))

print(var_df["Product Description"].value_counts())

### cloud not singletons
var_df_shell=var_df[var_df["Occupancy"]>1]
vc2=var_df_shell["Product Description"].value_counts()

fig,ax=plt.subplots()
ax.bar(vc2.index, vc2.values, color="darkgreen")
ax.set_xlabel("Description")
ax.set_ylabel("Count")
plt.xticks(rotation=30, ha="right")
plt.subplots_adjust(bottom=0.6, left=0.2)
plt.show()
fig.savefig("PSEUDO/Graphs/no_flank_cloud_description.png", dpi=300)

bed_df = bed_dict["Dd2"]
chr_bed = bed_df[bed_df["chrom"] == "PfDd2_04"]
print(chr_bed)

start, end = 904261, 913085
in_core = chr_bed[(chr_bed["name"].str.startswith("Core")) & (chr_bed["start"] <= start) & (chr_bed["end"] >= end)]
in_var = chr_bed[(chr_bed["name"].str.startswith("Var")) & (chr_bed["start"] <= start) & (chr_bed["end"] >= end)]
print("in_core:", in_core)
print("in_var:", in_var)


bed_df = bed_dict["SN01"]
chr_bed = bed_df[bed_df["chrom"] == "PfSN01_13"]
print(chr_bed)

import pandas as pd
data = pd.read_csv("GET_PANGENES_pseudo/no_flank_unmapped_genes.tsv", sep="\t")
row = data[data["Gene ID"] == "PfSN01_130005000"]
print(row)


row = final_df[final_df["Gene ID"] == "PfSN01_130005000"]
print(row[["Gene ID", "Genome", "Chromosome", "Start Position", "End Position", "Location"]])