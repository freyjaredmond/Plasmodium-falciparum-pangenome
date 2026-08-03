import pandas as pd
from pathlib import Path
import re

gene_id_list = ["PF3D7_0420100","PF3D7_1352100","PF3D7_1470700","PF3D7_1313800","PF3D7_1117700","PF3D7_0423700","PF3D7_1108500",
                "PF3D7_1032400","PF3D7_0607300","PF3D7_0710900"]

#define the confidence and biological importance scoring
def extract_percentile(pct_str):    #extracts the score from the percentile text
    if pd.isna(pct_str):
        return None
    m = re.search(r'(\d+\.?\d*)', str(pct_str))
    return float(m.group(0)) if m else None

def bio_score(pct):
    if pct is None or pd.isna(pct): return None
    if pct > 50: return 0
    elif pct > 40: return 1
    elif pct > 30: return 2
    elif pct > 20: return 3
    elif pct > 10: return 4
    else: return 5

def confidence_score(p):
    if p is None or pd.isna(p):
        return "DE not available"
    p = abs(float(p))
    if p > 0.05: return 0
    elif p < 0.00001: return 5
    elif p < 0.0001: return 4
    elif p < 0.001: return 3
    elif p < 0.01: return 2
    else: return 1

#---------------------------#    
#       Fold Change         #
#---------------------------#
for gene in gene_id_list:
    print(f"Extracting data for:{gene}")
    fc_table = []
    folder_path = Path("LFC studies")

    for file_path in folder_path.glob("*.txt"):
        with open(file_path, 'r') as f:
            study_name = f.readline().strip()
            description = f.readline().strip()
            comparison = f.readline().strip()

        data = pd.read_csv(file_path, sep="\t", skiprows=3)
        total_genes = len(data)
        #rank the reference expression
        data["Ref"]=pd.to_numeric(data["Chosen Ref (floor)"].str.split("(").str[0],errors="coerce")
        data["Expression Rank"] = data["Ref"].rank(method="min", ascending=False)
        data["Expression Percentile"] = (data["Expression Rank"] / len(data)) * 100
        #split fold changes into negative and positive
        data["Fold Change"] = pd.to_numeric(data["Fold Change"])
        upregulated = data[data["Fold Change"] > 0].copy()
        downregulated = data[data["Fold Change"] < 0].copy()
        no_change = data[data["Fold Change"] == 0].copy()

        upregulated["up_rank"] = upregulated["Fold Change"].rank(method="min", ascending=False)
        upregulated["percentile"] = (upregulated["up_rank"] / len(upregulated)) * 100

        downregulated["down_rank"] = downregulated["Fold Change"].rank(method="min", ascending=True)
        downregulated["percentile"] = (downregulated["down_rank"] / len(downregulated)) * 100

        no_change["up_rank"] = None
        no_change["down_rank"] = None
        no_change["percentile"] = None

        data = pd.concat([upregulated, downregulated, no_change]).sort_index()

        gene_row = data[data["Gene ID"] == gene]
        if gene_row.empty:
            print(f"Gene not found in {study_name}")
            continue  #genes are not always in the study
        #extract the values
        ref = gene_row["Chosen Ref (floor)"].values[0]
        comp = gene_row["Chosen Comp (floor)"].values[0]
        ref_rank=gene_row["Expression Rank"].values[0]
        ref_per=gene_row["Expression Percentile"].values[0]
        FC = gene_row["Fold Change"].values[0]
        percentile = gene_row["percentile"].values[0]
        up_rank = None
        down_rank = None
        #define fc percentiles
        if FC > 0:
            up_rank = gene_row["up_rank"].values[0]
            sig_desc = f"Top {percentile:.1f}% of upregulated genes"
            sig_desc_total = len(upregulated)
        elif FC < 0:
            down_rank = gene_row["down_rank"].values[0]
            sig_desc = f"Top {percentile:.1f}% of downregulated genes"
            sig_desc_total = len(downregulated)
        else:
            sig_desc = "No change (FC = 0)"
            sig_desc_total = len(no_change)

        #build the tsv

        fc_table.append({
            'Study': study_name,
            'Description': description,
            'Condition': comparison,
            'RNA-seq Reference (floor)': ref,
            'RNA-seq Comparison (floor)': comp,
            "RNA-seq Ref Expression Rank": ref_rank,
            "RNA-seq Ref Expression Percentile":ref_per,
            'RNA-seq Fold Change': FC,
            'RNA-seq Fold Change Up Rank': up_rank,
            'RNA-seq Fold Change Down Rank': down_rank,
            'RNA-seq Fold Change Percentile': sig_desc,
            'RNA-seq Fold Change Rank size': sig_desc_total,
        })

    results_df = pd.DataFrame(fc_table)
    results_df = results_df.set_index(['Study', 'Description', 'Condition'])

    #---------------------------#
    #  Differential Expression  #
    #---------------------------#

    de_table = []
    folder_path2 = Path("DE studies")

    for file_path in folder_path2.glob("*.txt"):
        with open(file_path, 'r') as f:
            study_name = f.readline().strip()
            description = f.readline().strip()
            comparison = f.readline().strip()

        data = pd.read_csv(file_path, sep="\t", skiprows=3)
        data.columns = data.columns.str.strip()

        gene_row = data[data["Gene ID"] == gene]
        if gene_row.empty:
            print(f"Gene not found in {study_name}")
            continue

        p = gene_row["P-Value"].values[0]
        e = gene_row["Effect Size"].values[0]

        # P-value ranking
        sigpval = data[data["P-Value"] < 0.05].copy()
        nonsigpval = data[data["P-Value"] >= 0.05].copy()

        sigpval["sig_rank"] = sigpval["P-Value"].rank(method="min", ascending=True)
        sigpval["sig_percentile"] = (sigpval["sig_rank"] / len(sigpval)) * 100

        nonsigpval["sig_rank"] = None
        nonsigpval["sig_percentile"] = None

        data_p = pd.concat([sigpval, nonsigpval]).sort_index()
        gene_row_p = data_p[data_p["Gene ID"] == gene]

        rank = None
        if p < 0.05:
            rank = gene_row_p["sig_rank"].values[0]
            percentile_p = gene_row_p["sig_percentile"].values[0]
            sig_p = f"Top {percentile_p:.1f}% of significant genes"
            sig_p_total = len(sigpval)
        else:
            sig_p = "Not significant"
            sig_p_total = len(nonsigpval)

        de_table.append({
            'Study': study_name,
            'Description': description,
            'Condition': comparison,
            'P_value': p,
            'P-value rank': rank,
            'P-value Percentile': sig_p,
            'Number of significant genes': sig_p_total,
            'Effect_size': e
        })

    de_df = pd.DataFrame(de_table)
    de_df = de_df.set_index(['Study', 'Description', 'Condition'])

    #---------------------------#
    #           Array           #
    #---------------------------#
    array_table = []
    folder_path3 = Path("Array")

    for file_path in folder_path3.glob("*.txt"):
        with open(file_path, 'r') as f:
            study_name = f.readline().strip()
            description = f.readline().strip()
            comparison = f.readline().strip()

        data = pd.read_csv(file_path, sep="\t", skiprows=3)
        data.columns = data.columns.str.strip()
        total_genes = len(data)
        #get ref expression percentiles
        if "Chosen Ref (log2)" in data.columns:
            data["Ref"]=pd.to_numeric(data["Chosen Ref (log2)"])
        elif "Chosen Ref" in data.columns:
             data["Ref"]=pd.to_numeric(data["Chosen Ref"])
        data["Expression Rank"] = data["Ref"].rank(method="min", ascending=False)
        data["Expression Percentile"] = (data["Expression Rank"] / len(data)) * 100

        # Rename Fold Difference to Fold Change if needed
        data.columns = data.columns.str.replace("Fold Difference", "Fold Change")

        data["Fold Change"] = pd.to_numeric(data["Fold Change"], errors="coerce")
        mean_fc = data["Fold Change"].mean()
        total_sd = data["Fold Change"].std()


        upregulated = data[data["Fold Change"] > 0].copy()
        downregulated = data[data["Fold Change"] < 0].copy()
        no_change = data[data["Fold Change"] == 0].copy()

        upregulated["up_rank"] = upregulated["Fold Change"].rank(method="min", ascending=False)
        upregulated["percentile"] = (upregulated["up_rank"] / len(upregulated)) * 100

        downregulated["down_rank"] = downregulated["Fold Change"].rank(method="min", ascending=True)
        downregulated["percentile"] = (downregulated["down_rank"] / len(downregulated)) * 100

        no_change["up_rank"] = None
        no_change["down_rank"] = None
        no_change["percentile"] = None

        data = pd.concat([upregulated, downregulated, no_change]).sort_index()

        gene_row = data[data["Gene ID"] == gene]
        if gene_row.empty:
            print(f"Gene not found in {study_name}")
            continue

        # Handle different ref/comp column names
        if "Chosen Ref (log2)" in data.columns:
            ref = gene_row["Chosen Ref (log2)"].values[0]
            comp = gene_row["Chosen Comp (log2)"].values[0]
            ref_log = ref
            comp_log = comp

        elif "Chosen Ref" in data.columns:
            ref = gene_row["Chosen Ref"].values[0]
            comp = gene_row["Chosen Comp"].values[0]
            ref_log = None
            comp_log = None

        else:
            print(f"No ref/comp column found in {file_path.name}")
            continue

        FC = gene_row["Fold Change"].values[0]
        percentile = gene_row["percentile"].values[0]
        ref_rank=gene_row["Expression Rank"].values[0]
        ref_percentile=gene_row["Expression Percentile"].values[0]
        up_rank = None
        down_rank = None

        if FC > 0:
            up_rank = gene_row["up_rank"].values[0]
            sig_desc = f"Top {percentile:.1f}% of upregulated genes"
            sig_desc_total = len(upregulated)
        elif FC < 0:
            down_rank = gene_row["down_rank"].values[0]
            sig_desc = f"Top {percentile:.1f}% of downregulated genes"
            sig_desc_total = len(downregulated)
        else:
            sig_desc = "No change (FC = 0)"
            sig_desc_total = len(no_change)

        array_table.append({
            'Study': study_name,
            'Description': description,
            'Condition': comparison,
            'Microarray Reference': ref,
            "Microarray Reference Expression Rank":ref_rank,
            "Microarray Reference Expression Percentile":ref_percentile,
            'Microarray Comparison': comp,
            'Microarray Reference (log2)': ref_log,
            'Microarray Comparison (log2)': comp_log,
            'Microarray Fold Change': FC,
            'Microarray Fold Change Up Rank': up_rank,
            'Microarray Fold Change Down Rank': down_rank,
            'Microarray Fold Change Percentile': sig_desc,
            'Microarray Fold Change Rank size': sig_desc_total,

        })
    array_df=pd.DataFrame(array_table)
    array_df = array_df.set_index(['Study', 'Description', 'Condition'])

    #---------------------------#
    #           Merge           #
    #---------------------------#




    merged_df = results_df.merge(de_df, left_index=True, right_index=True, how="outer")
    merged_df2 = merged_df.merge(array_df, left_index=True, right_index=True, how="outer")
   #---------------------------#
    #           Score           #
    #----------------------------#


    merged_df2["Biological Importance Score"] = merged_df2["RNA-seq Fold Change Percentile"].apply(
        lambda x: bio_score(extract_percentile(x))
    ).combine_first(
        merged_df2["Microarray Fold Change Percentile"].apply(
            lambda x: bio_score(extract_percentile(x))))  #use apply to do a function down a column, combine first fills the column with rna-seq and then fills the rest with microarray
        


    merged_df2["Confidence Score"] = merged_df2["P_value"].apply(confidence_score)


    merged_df2 = merged_df2.reset_index()
    merged_df2 = merged_df2.sort_values(['Study', 'Condition']).reset_index(drop=True)

    # only keep description on first occurrence of each study
    merged_df2['Description'] = merged_df2['Description'].where(
        ~merged_df2['Study'].duplicated(), 
        other=''
    )

    merged_df2.to_csv(f"transcriptomics_data/{gene}_transcriptomics_data.tsv", sep="\t", index=False)