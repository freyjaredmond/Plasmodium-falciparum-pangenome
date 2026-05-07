# This script processes LiftOff and GffCompare outputs for P. falciparum genome assemblies.
# It extracts genes with valid_ORF=1 from the LiftOff polished GFF3 file and filters the GffCompare tracking file accordingly, classifying entries by their ORF status.
# A bar chart of valid_ORF counts is produced alongside a summary of GffCompare tracking code frequencies, which are written to TSV files and visualised as bar charts.
# Input: LiftOff polished GFF3 file, GffCompare tracking file
# Output: filtered TSV, classified TSV, ORF bar chart, tracking code bar chart


import pandas as pd
import matplotlib.pyplot as plt
#### get a list of gene ids that have valid_orfs
def extract_valid(liftoff_gff_polished):
    valid_genes=[]
    invalid_genes=[]
    with open (liftoff_gff_polished, "r") as f:
        for lines in f:
            if lines.startswith("#"): 
                continue
            field=lines.strip().split("\t")
            if field [2]=="protein_coding_gene": #only protein coding has valid_orf attribute
                attributes=field[8]
                attributes_dict={}
                for part in attributes.split(";"):
                    if "=" in part:
                        key,value= part.strip().split("=",1)
                        attributes_dict[key]=value
                gene_id=attributes_dict.get("ID")
                orf_status=attributes_dict.get("valid_ORFs")
                if gene_id and orf_status=="1":
                    valid_genes.append(gene_id)
                elif gene_id and orf_status=="0":
                    invalid_genes.append(gene_id)

    return valid_genes, invalid_genes

### filter the tracking file for these genes
def filter_tracking (tracking_file, valid_list,invalid_list,plasmodium,output_dir):
    out_filtered = f"{output_dir}/{plasmodium}_filtered_valid_orf.tsv" #tsv that only has valid orf=1
    out_classified = f"{output_dir}/{plasmodium}_tracking_with_orf_classification.tsv"
    total=0
    kept=0
    orf_zero=0
    removed_no_orf=0
    removed_no_gene_id=0
    unique_kept_genes=set()#only keeps unique
    unique_kept_genes_removed=set()
    with open(tracking_file, "r") as f, \
         open(out_filtered, "w") as out_f, \
         open(out_classified, "w") as out_c: 
        for lines in f:
            total+=1
            part=lines.strip().split("\t")
            id=part[4].split("q1:")[1]
            gene_id=id.split("|")[0] 
            if gene_id and gene_id in valid_list:
                out_f.write(lines)
                out_c.write(lines.strip() + "\tvalid_ORF=1\n")
                kept+=1
                unique_kept_genes.add(gene_id)
            elif gene_id and gene_id in invalid_list:
                out_c.write(lines.strip() + "\tvalid_ORF=0\n")
                orf_zero+=1
                unique_kept_genes_removed.add(gene_id)
            elif gene_id:
                out_c.write(lines.strip() + "\tno_ORF_status\n")
                removed_no_orf+=1
            else:
                out_c.write(lines.strip() + "\tno_gene_id\n")
                removed_no_gene_id+=1
                
    
    print(f"Total: {total}\nKept: {kept}\nValid_ORF=0: {orf_zero}\nNo ORF status: {removed_no_orf}\nInvalid gene id: {removed_no_gene_id}\nUnique kept: {len(unique_kept_genes)}\nRemoved unique: {len(unique_kept_genes_removed)}")
    return out_filtered,out_classified

#extract orf counts for the polished gff 
def extract_plot(plasmodium,gff,output_dir):
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
                elif orf=="0":
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
    fig.savefig(f"{output_dir}/{plasmodium}_orf_bar_polished.png", dpi=300)
def tracking_count(plasmodium,tracking,outdir):
    counts={}
    #count the codes
    with open (tracking, "r") as f:
        for lines in f:
            line=lines.split("\t")
            code=line[3]
            if code in counts:
                counts[code] += 1 #
            else:
                counts[code] = 1
     #write the codes out as a tsv       
    out_file = f"{outdir}/{plasmodium}_tracking_code_counts_filtered.tsv"
    with open(out_file, "w") as out:
        out.write("tracking_code\tcount\n") #column headers
        for code, count in counts.items():
            out.write(f"{code}\t{count}\n")
    fig,ax=plt.subplots()
    colours = plt.cm.tab10.colors #gives 10 colours
    bar=ax.bar(counts.keys(),counts.values(), color=colours[:len(counts)])
    ax.set_xlabel("Tracking code")
    ax.set_ylabel("Counts")
    ax.set_title(f"Frequency of tracking counts for {plasmodium}")
    ax.bar_label(bar)
    fig.savefig(f"{outdir}/{plasmodium}_tracking_counts_bar_filtered.png",dpi=300)

##### use the script
valid_list,invalid_list=extract_valid("Lift_Off/LiftOff_Output/pfCD01/pfCD01_liftover.gff3_polished")
tracking_filtered,tracking_class=filter_tracking("Lift_Off/LiftOff_Output/pfCD01/gff_compare_out/pfCD01_original_vs_pfCD01_gffcomp.tracking",valid_list,invalid_list,"pfCD01","Lift_Off/LiftOff_Output/pfCD01/gff_compare_out/orf_analysis")
extract_plot("pfCD01","Lift_Off/LiftOff_Output/pfCD01/pfCD01_liftover.gff3_polished","Lift_Off/LiftOff_Output/pfCD01/gff_compare_out/orf_analysis")
tracking_count("pfCD01",tracking_filtered,"Lift_Off/LiftOff_Output/pfCD01/gff_compare_out/orf_analysis")


            

            
                
                
                
