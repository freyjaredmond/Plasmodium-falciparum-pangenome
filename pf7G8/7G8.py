import matplotlib.pyplot as plt
def extract_plot(plasmodium,gff):
    valid_orf=0
    no_orf=0   #store as a counter
    coverage_list=[]#store as a list
    with open (gff, "r") as f:
        for lines in f:
            if lines.startswith("#"): #ignore comments
                continue
            field=lines.split("\t")
            if field [2]=="protein_coding_gene": #only protein coding has valid_orf attribute
                attributes=field[8]
                attributes_dict={}
                for part in attributes.split(";"):# cant use indexing as attribute order may change
                    if "=" in part:
                        key,value= part.split("=")
                        attributes_dict[key]=value
                orf=attributes_dict.get("valid_ORFs")#.get doesnt throw an error is its not there
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
    fig.savefig(f"{plasmodium}_orf_bar_polished.png", dpi=300)

#histogram
    fig,ax=plt.subplots()
    ax.hist(coverage_list,bins=50, color="red")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Coverage")
    ax.set_title(f"Histogram of the coverage of the {plasmodium} liftoff")
    fig.savefig(f"{plasmodium}_cov_hist_png", dpi=300)

    print( valid_orf,no_orf)

extract_plot("pf7G8","pf7G8_liftover.gff3_polished")
