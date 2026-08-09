import pandas as pd
import glob
import re
import os
matrix = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/pangene_matrix_genes.tab", sep="\t", index_col=0)
matrix=matrix.drop("chr:unsorted", axis=1)
# Get the 3D7 row
d7_row = matrix.loc["PlasmoDB-68_Pfalciparum3D7"] #gves a series with column names as index

# Find clusters where 3D7 is absent
absent = d7_row[d7_row == "-"].index.tolist()

#get all the genes
absent_genes = []
for cluster in absent:
    for gene in matrix[cluster]:
        if gene != "-" and isinstance(gene, str):
            absent_genes.append(gene)
df=pd.DataFrame(absent_genes)
df.to_csv("PSEUDO/16_3D7_absent_all_pseudo", sep="\t", index=False)


### create the gffs

#map for genome prefixes (they dont all match)
prefix_to_genome = {
    "7G8-2": "7G8-2019",
    "NF135": "NF135C10",
    "7G8": "7G8",
    "CD01": "CD01",
    "Dd2": "Dd2",
    "GA01": "GA01",
    "GB4": "GB4",
    "GN01": "GN01",
    "HB3": "HB3",
    "IT": "IT",
    "KE01": "KE01",
    "KH01": "KH01",
    "KH02": "KH02",
    "NF166": "NF166",
    "NF54": "NF54",
    "SN01": "SN01",
    "TG01": "TG01",
    "ML01": "ML01",
    "SD01": "SD01",
}

files = glob.glob("GET_PANGENES_filtered/inputs_flat/*.gff")

os.makedirs("PSEUDO/16_absent_gffs_all_pseudo", exist_ok=True)
#for every genomes gff file, identify genes in the absent gene list that match prefixes ans extract relevant gff
for gff_file in files:
    basename = os.path.basename(gff_file)

    genome_genes = [g for g in absent_genes
                    if re.search(r'Pf([^_]+)_', g) and #catches anything up to the underscore
                    prefix_to_genome.get(re.search(r'Pf([^_]+)_', g).group(1), "") in basename]


    with open(gff_file) as inp, open(f"PSEUDO/16_absent_gffs_all_pseudo/{basename}_absent.gff", "w") as out:
        for line in inp:
            if line.startswith("#"):
                out.write(line)
                continue
            if len(line.strip().split("\t")) < 9:
                continue
            if any(g in line for g in genome_genes): #gets the gff of interest
                out.write(line)
