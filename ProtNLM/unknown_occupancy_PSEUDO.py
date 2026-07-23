import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats
import numpy as np

# get pangene occupancy
pangenome = pd.read_csv("PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)

pangenome_binary = (pangenome != "-").astype(int)

gene_occupancy = pangenome_binary.sum(axis=0)

occupancy_counts = gene_occupancy.value_counts().sort_index()

print("\nOccupancy counts:")
print(occupancy_counts)


def classify_colour(x):
    if x == 16:
        return "red"       # core
    elif x == 15:
        return "orange"    # soft-core
    elif x in (1, 2):
        return "blue"      # cloud
    else:
        return "green"     # shell

bar_colours = [classify_colour(x) for x in occupancy_counts.index]


# Read the product descriptions
annotations = pd.read_csv("GET_PANGENES_pseudo/product_des.txt", sep="\t", index_col=0)
print(annotations["Product Description"].value_counts())

# Some genes appear more than once — keep only the first row per gene ID
annotations = annotations[~annotations.index.duplicated(keep="first")]


# Define the keywords that indicate a gene has no known function
unknown_keywords = ["hypothetical", "hypothetical protein", "conserved protein, unknown function","conserved Plasmodium protein, unknown function","conserved Plasmodium membrane protein, unknown function"]

# True if product description matches unknown words
is_unknown = annotations["Product Description"].str.contains(
    "|".join(unknown_keywords), case=False, na=False
)
# Get the proportion of known/unknown for each pangenome occupancy

unknown_counts = {}
known_counts = {}
total_unknown=[]
for occ_val in occupancy_counts.index:


    genes_at_occ = gene_occupancy[gene_occupancy == occ_val].index


    unknown_flags = []
    for gene_id in genes_at_occ:
        if gene_id in is_unknown.index:
            unknown_flags.append(is_unknown[gene_id]) 
        else:
            unknown_flags.append(False)  

    n_unknown = sum(unknown_flags)
    total_unknown.append(n_unknown)


    n_known = occupancy_counts[occ_val] - n_unknown

    unknown_counts[occ_val] = n_unknown
    known_counts[occ_val] = n_known


unknown_series = pd.Series(unknown_counts).sort_index()
known_series = pd.Series(known_counts).sort_index()
# Plot

x_ticks = list(range(1, 17))
fig, ax = plt.subplots(figsize=(16, 8))


bar_known = ax.bar(known_series.index, known_series.values, color=bar_colours)

bar_unknown = ax.bar(unknown_series.index, unknown_series.values,
                     bottom=known_series.values, color="grey", alpha=0.6)

ax.set_xlabel("Pangene occupancy", fontsize=18)
ax.set_ylabel("Number of pangene clusters", fontsize=18)
ax.set_xticks(x_ticks)
ax.tick_params(axis='both', labelsize=16)
ax.set_ylim(0, 4700)
ax.set_xlim(left=0.5, right=16.5)

legend_elements = [
    Patch(facecolor="red",    label="Core"),
    Patch(facecolor="orange", label="Soft-core"),
    Patch(facecolor="green",  label="Shell"),
    Patch(facecolor="blue",   label="Cloud"),
    Patch(facecolor="grey",   alpha=0.6, label="Unknown / hypothetical"),
]
ax.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=16)

fig.savefig("PSEUDO/Graphs/Pangenome_occupancy_unknown.png", dpi=300, bbox_inches='tight')
plt.show()

print(sum(total_unknown))
