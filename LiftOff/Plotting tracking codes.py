# This script reads a GffCompare tracking file for a given P. falciparum genome assembly and counts the frequency of each GffCompare classification code (e.g. =, k, j, o).
# It produces:
# 1. A TSV file of tracking code counts
# 2. A bar chart of tracking code frequencies
# Input: GffCompare tracking file
# Output: tracking code counts TSV, bar chart PNG

import matplotlib.pyplot as plt
def tracking_count(plasmodium,tracking):
    counts={}
    #count the codes
    with open (tracking, "r") as f:
        for lines in f:
            line=lines.split("\t")
            tracking=line[3]
            if tracking in counts:
                counts[tracking] += 1 #adds one to the dict if already there
            else:
                counts[tracking] = 1
     #write the codes out as a tsv       
    out_file = f"{plasmodium}_tracking_code_counts.tsv"
    with open(out_file, "w") as out:
        out.write("tracking_code\tcount\n") #column headers
        for code, count in counts.items():
            out.write(f"{code}\t{count}\n")
    fig,ax=plt.subplots()
    colours = plt.cm.tab10.colors #gives 10 colours
    bar=ax.bar(counts.keys(),counts.values(), color=colours[:len(counts)])#filters colour list by the number of codes
    ax.set_xlabel("Tracking code")
    ax.set_ylabel("Counts")
    ax.set_title(f"Frequency of tracking counts for {plasmodium}")
    ax.bar_label(bar)
    fig.savefig(f"{plasmodium}_tracking_counts_bar.png",dpi=300)
tracking_count("pfCD01", "pfCD01_original_vs_pfCD01_gffcomp.tracking")
