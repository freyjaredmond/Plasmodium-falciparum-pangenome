import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats
import numpy as np


pangenome = pd.read_csv("GET_PANGENES/PSEUDO/GET_PANGENES_OUTPUT_16_PSEUDO/Clusters_renamed_pseudo.tsv", sep="\t", index_col=0)

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
annotations = pd.read_csv("GET_PANGENES/GET_PANGENES_pseudo/product_des.txt", sep="\t", index_col=0)
print(annotations["Product Description"].value_counts())

# Some genes appear more than once — keep only the first row per gene ID
annotations = annotations[~annotations.index.duplicated(keep="first")]


# Define the keywords that indicate a gene has no known function
unknown_keywords = ["hypothetical", "hypothetical protein", "conserved protein, unknown function","conserved Plasmodium protein, unknown function","conserved Plasmodium membrane protein, unknown function"]

# Create a True/False Series: True if the gene's description matches any keyword
is_unknown = annotations["Product Description"].str.contains(
    "|".join(unknown_keywords), case=False, na=False
)


unknown_counts = {}
known_counts = {}
total_unknown=[]
for occ_val in occupancy_counts.index:


    genes_at_occ = gene_occupancy[gene_occupancy == occ_val].index


    unknown_flags = []
    for gene_id in genes_at_occ:
        if gene_id in is_unknown.index:
            unknown_flags.append(is_unknown[gene_id])  # True or False
        else:
            unknown_flags.append(False)  # gene not in annotations, treat as known

    # Step 8c: count the Trues (True = 1, False = 0)
    n_unknown = sum(unknown_flags)
    total_unknown.append(n_unknown)

    # Step 8d: known = total at this occupancy minus the unknowns
    n_known = occupancy_counts[occ_val] - n_unknown

    unknown_counts[occ_val] = n_unknown
    known_counts[occ_val] = n_known

# Convert dictionaries to Series sorted by occupancy (1 → 16) for plotting
unknown_series = pd.Series(unknown_counts).sort_index()
known_series = pd.Series(known_counts).sort_index()

print(sum(total_unknown))

print(f"Total clusters at occupancy 16: {occupancy_counts[16]}")
print(f"Unknown/hypothetical at occupancy 16: {unknown_counts[16]}")


#######################
# Evidence source distribution across the 3D7 proteome (bar chart)

evidence_df = pd.read_csv("Function_of_proteins/ProtNLM/uniprotkb_proteome_UP000001450_2026_03_06_protein_descriptions.tsv", sep="\t")

organism = evidence_df["organism"].unique()[0]
source_counts = evidence_df["evidenceSource"].value_counts()

# Filter out N/A if it exists
if "N/A" in source_counts.index:
    source_counts = source_counts.drop("N/A")

# Take top 15 sources
source_counts = source_counts.head(15)

total_evidence = len(evidence_df)

### Plot the curated scores
curated_scored=pd.read_excel("Function_of_proteins/ProtNLM/Supplementary_data_A.xlsx", sheet_name="ProtNLM vs Curated genes")
curated_scored.columns = curated_scored.columns.str.strip()
score_dict={1:"Exact Match",2:"Similar Match",3:"Partial Match",4:"Match in ranks 2-3",5:"Match in ranks 4-10",6:"No match in any rank"}

score_counts = curated_scored["Score"].value_counts().sort_index()
bar_labels = [score_dict[s] for s in score_counts.index]


#### Plot unknown scores
unknown_scored=pd.read_excel("Function_of_proteins/ProtNLM/Supplementary_data_A.xlsx", sheet_name="ProtNLM unknown proteins")
unknown_scored.columns = unknown_scored.columns.str.strip()
unknown_dict={1:"Unknown",2:"Non-specific",3:"Specific",4:"Exact"}

unknown_score_counts = unknown_scored["Score"].value_counts().sort_index()
unknown_bar_labels = [unknown_dict[s] for s in unknown_score_counts.index]

## blast plot
####mean plot
one=pd.read_excel("Function_of_proteins/ProtNLM/Supplementary_data_A.xlsx", sheet_name="Babesia ovis set 1")
two=pd.read_excel("Function_of_proteins/ProtNLM/Supplementary_data_A.xlsx", sheet_name="Babesia ovis set 2")
three=pd.read_excel("Function_of_proteins/ProtNLM/Supplementary_data_A.xlsx", sheet_name="Babesia ovis set 3")

blast_score_dic={"1a":"Both Match","1b":"Both Matach Partially","2a":"ProtNLM Better Match","2b":"ProtNLM Only Match","3a":"BLAST Better Match","3b":"BLAST Only Match","4a":"Neither Match (same)","4b":"Neither Match (different)","5":"Uncharacterised"}
counts1=one["Score"].value_counts().reset_index()
counts2=two["Score"].value_counts().reset_index()
counts3=three["Score"].value_counts().reset_index()
counts1.columns=["Score","Counts"]
counts2.columns=["Score","Counts"]
counts3.columns=["Score","Counts"]
counts1["Score"] = counts1["Score"].astype(str)
counts2["Score"] = counts2["Score"].astype(str)
counts3["Score"] = counts3["Score"].astype(str)

merged=counts1.merge(counts2, on="Score", how="outer")
merged=merged.merge(counts3, on="Score", how="outer")

print(merged.head())

merged['Mean'] = merged[['Counts_x', 'Counts_y', 'Counts']].mean(axis=1)
merged['Std'] = merged[['Counts_x', 'Counts_y', 'Counts']].std(axis=1)

blast_bar_labels = [blast_score_dic[s] for s in merged['Score']]
print(merged)


#######################
# Combined 2x3 panel figure — plot A spans the full top row

fig = plt.figure(figsize=(8.27, 11.69), constrained_layout=True)
gs = fig.add_gridspec(3, 2)

ax_a = fig.add_subplot(gs[0, :])
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[1, 1])
ax_d = fig.add_subplot(gs[2, 0])
ax_e = fig.add_subplot(gs[2, 1])

panel_letter_kwargs = dict(fontsize=22, fontweight="bold")

# A: pangene occupancy vs unknown/hypothetical
x_ticks = list(range(1, 17))

bar_known = ax_a.bar(known_series.index, known_series.values, color=bar_colours)
bar_unknown = ax_a.bar(unknown_series.index, unknown_series.values,
                        bottom=known_series.values, color="grey", alpha=0.6)

ax_a.set_xlabel("Pangene occupancy", fontsize=14)
ax_a.set_ylabel("Number of pangene clusters", fontsize=14)
ax_a.set_xticks(x_ticks)
ax_a.tick_params(axis='both', labelsize=12)
ax_a.set_ylim(0, 4700)
ax_a.set_xlim(left=0.5, right=16.5)

legend_elements = [
    Patch(facecolor="red",    label="Core"),
    Patch(facecolor="orange", label="Soft-core"),
    Patch(facecolor="green",  label="Shell"),
    Patch(facecolor="blue",   label="Cloud"),
    Patch(facecolor="grey",   alpha=0.6, label="Unknown / hypothetical"),
]
ax_a.legend(handles=legend_elements, bbox_to_anchor=(0.5, -0.32), loc="upper center", ncol=5, fontsize=10)
ax_a.text(-0.08, 1.1, "A", transform=ax_a.transAxes, **panel_letter_kwargs)

# B: evidence source distribution across the 3D7 proteome
bars_b = ax_b.barh(range(len(source_counts)), source_counts.values, color="steelblue", edgecolor="black", linewidth=0.5)

ax_b.set_yticks(range(len(source_counts)))
ax_b.set_yticklabels(source_counts.index, fontsize=9)
ax_b.set_xlabel("Number of Proteins", fontsize=12, fontweight="bold")
ax_b.set_ylabel("Evidence Source", fontsize=12, fontweight="bold")
ax_b.text(-0.1, 1.05, "B", transform=ax_b.transAxes, **panel_letter_kwargs)

# C: curated genes score distribution
print("****")
print(score_counts)
ax_c.bar(bar_labels, score_counts.values, color=["darkgreen", "lightgreen"])
ax_c.set_xlabel("Score")
ax_c.set_ylabel("Count")
ax_c.tick_params(axis='x', rotation=30)
for label in ax_c.get_xticklabels():
    label.set_ha("right")
ax_c.text(-0.1, 1.05, "C", transform=ax_c.transAxes, **panel_letter_kwargs)

# D: unknown genes score distribution
print(unknown_score_counts)
ax_d.bar(unknown_bar_labels, unknown_score_counts.values, color=["darkgreen", "lightgreen"])
ax_d.set_xlabel("Score")
ax_d.set_ylabel("Count")
ax_d.tick_params(axis='x', rotation=30)
for label in ax_d.get_xticklabels():
    label.set_ha("right")
ax_d.text(-0.1, 1.05, "D", transform=ax_d.transAxes, **panel_letter_kwargs)

# E: ProtNLM vs BLAST (Babesia ovis, UniRef90), mean across three random samples
ax_e.bar(blast_bar_labels, merged['Mean'],
         yerr=merged['Std'],
         color=["lightgreen", "darkgreen"],
         alpha=0.7)
ax_e.set_xlabel("Score")
ax_e.set_ylabel("Counts")
ax_e.tick_params(axis='x', rotation=30)
for label in ax_e.get_xticklabels():
    label.set_ha("right")
ax_e.text(-0.1, 1.05, "E", transform=ax_e.transAxes, **panel_letter_kwargs)

fig.savefig("GET_PANGENES/PSEUDO/GRAPHS/protnlm_panel.png", dpi=600, bbox_inches="tight", pad_inches=0.3)
plt.show()
