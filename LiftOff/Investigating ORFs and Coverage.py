# This script reads a LiftOff polished GFF3 file for a given P. falciparum genome assembly and extracts valid_ORF status and coverage values for all protein coding genes.
# It produces two figures:
# 1. A bar chart showing the frequency of genes with valid_ORF=1 and valid_ORF=0
# 2. A histogram of LiftOff coverage values across all protein coding genes
# Input: LiftOff polished GFF3 file
# Output: bar chart PNG, coverage histogram PNG

import matplotlib.pyplot as plt
def extract_plot(plasmodium,gff):
    valid_orf=0
    no_orf=0   #store as a counter
    coverage_list=[]#store as a list
    with open (gff, "r") as f:
        for lines in f:
            if lines.startswith("#"): 
                continue
            field=lines.split("\t")
            if field [2]=="protein_coding_gene": 
                attributes=field[8]
                attributes_dict={}
                for part in attributes.split(";"):
                    if "=" in part:
                        key,value= part.split("=")
                        attributes_dict[key]=value
                orf=attributes_dict.get("valid_ORFs")
                if orf=="1":
                    valid_orf+=1
                if orf=="0":
                    no_orf+=1
                coverage=attributes_dict.get("coverage")
                coverage_list.append(float(coverage))
 
    ## bar
    fig,ax=plt.subplots()
    bar=ax.bar(["valid_ORFs=1", "valid_orfs=0"], [valid_orf, no_orf], color=["green", "yellow"])
    ax.set_xlabel("ORF Class")
    ax.set_ylabel("Frequency")
    ax.bar_label(bar)
    ax.set_title(f"Frequency of valid ORFs for {plasmodium} liftoff")
    fig.savefig(f"{plasmodium}_orf_bar.png", dpi=300)

#histogram
    fig,ax=plt.subplots()
    ax.hist(coverage_list,bins=50, color="red")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Coverage")
    ax.set_title(f"Histogram of the coverage of the {plasmodium} liftoff")
    fig.savefig(f"{plasmodium}_cov_hist.png", dpi=300)

    print( valid_orf,no_orf)

