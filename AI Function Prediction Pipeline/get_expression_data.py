# This script extracts the transcritomics, proteomics, PTM and mutagenesis data for all genes
import pandas as pd
from pathlib import Path
import re
import os
import glob
gene_id_df=pd.read_csv("unknown_genes.tsv", sep="\t")
gene_id_list=gene_id_df["gene_id"].to_list()

peptide_count=pd.read_csv("Peptide_counts.txt", sep="\t")
###  Transcriptomics  ###
#########################
  
### Fold Change ###

for gene in gene_id_list:
    fc_table = []
    folder_path = Path("LFC studies")
    # extract the study description and comparisons from the txt files
    for file_path in folder_path.glob("*.txt"):
        with open(file_path, 'r') as f:
            study_name = f.readline().strip()
            description = f.readline().strip()
            comparison = f.readline().strip()

        data = pd.read_csv(file_path, sep="\t", skiprows=3)
        total_genes = len(data)
        data["Fold Change"] = pd.to_numeric(data["Fold Change"])
        data["Ref"]=pd.to_numeric(data["Chosen Ref (floor)"].str.split("(").str[0],errors="coerce")
        data["Expression Rank"] = data["Ref"].rank(method="min", ascending=False)
        data["Expression Percentile"] = (data["Expression Rank"] / len(data)) * 100
        # seperate into up and downregulated genes
        upregulated = data[data["Fold Change"] > 0].copy()
        downregulated = data[data["Fold Change"] < 0].copy()
        no_change = data[data["Fold Change"] == 0].copy()
        # rank and get the percentiles
        upregulated["up_rank"] = upregulated["Fold Change"].rank(method="min", ascending=False)
        upregulated["percentile"] = (upregulated["up_rank"] / len(upregulated)) * 100

        downregulated["down_rank"] = downregulated["Fold Change"].rank(method="min", ascending=True)
        downregulated["percentile"] = (downregulated["down_rank"] / len(downregulated)) * 100

        no_change["up_rank"] = None
        no_change["down_rank"] = None
        no_change["percentile"] = None
        # combine the dfs 
        data = pd.concat([upregulated, downregulated, no_change]).sort_index()
        # extract the gene
        gene_row = data[data["Gene ID"] == gene]
        if gene_row.empty:
            print(f"Gene not found in {study_name}")
            continue  
        # extract the neccessary data
        ref = gene_row["Chosen Ref (floor)"].values[0]
        comp = gene_row["Chosen Comp (floor)"].values[0]
        FC = gene_row["Fold Change"].values[0]
        percentile = gene_row["percentile"].values[0]
        exp_rank=gene_row["Expression Rank"].values[0]
        exp_percentile=gene_row["Expression Percentile"].values[0]
        up_rank = None
        down_rank = None
        # get the neccessary ranking
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
        # build the table
        fc_table.append({
            'Study': study_name,
            'Description': description,
            'Condition': comparison,
            'RNA-seq Reference (floor)': f'{ref}',
            "Expression Rank":exp_rank,
            "Expression Percentile":f"{exp_percentile} %",
            'RNA-seq Comparison (floor)': f'{comp}',
            'RNA-seq Fold Change': f'{FC}',
            'RNA-seq Fold Change Up Rank': up_rank,
            'RNA-seq Fold Change Down Rank': down_rank,
            'RNA-seq Fold Change Percentile': sig_desc,
            'RNA-seq Fold Change Rank size': sig_desc_total,
        })

    if fc_table:
        results_df = pd.DataFrame(fc_table)
        results_df = results_df.set_index(['Study', 'Description', 'Condition'])
    else:
        results_df = pd.DataFrame(columns=['Study', 'Description', 'Condition'])
        results_df = results_df.set_index(['Study', 'Description', 'Condition'])

   
    ### Differential Expression ###
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

        # Effect size ranking
        upregulated_es = data[data["Effect Size"] > 0].copy()
        downregulated_es = data[data["Effect Size"] < 0].copy()
        no_change_es = data[data["Effect Size"] == 0].copy()

        upregulated_es["up_rank"] = upregulated_es["Effect Size"].rank(method="min", ascending=False)
        upregulated_es["percentile"] = (upregulated_es["up_rank"] / len(upregulated_es)) * 100

        downregulated_es["down_rank"] = downregulated_es["Effect Size"].rank(method="min", ascending=True)
        downregulated_es["percentile"] = (downregulated_es["down_rank"] / len(downregulated_es)) * 100

        no_change_es["up_rank"] = None
        no_change_es["down_rank"] = None
        no_change_es["percentile"] = None

        data_es = pd.concat([upregulated_es, downregulated_es, no_change_es]).sort_index()
        gene_row_es = data_es[data_es["Gene ID"] == gene]

        up_rank_es = None
        down_rank_es = None

        if e > 0:
            up_rank_es = gene_row_es["up_rank"].values[0]
            percentile_es = gene_row_es["percentile"].values[0]
            sig_desc = f"Top {percentile_es:.1f}% of upregulated genes"
            sig_desc_total = len(upregulated_es)
        elif e < 0:
            down_rank_es = gene_row_es["down_rank"].values[0]
            percentile_es = gene_row_es["percentile"].values[0]
            sig_desc = f"Top {percentile_es:.1f}% of downregulated genes"
            sig_desc_total = len(downregulated_es)
        else:
            sig_desc = "No change (Effect Size = 0)"
            sig_desc_total = len(no_change_es)

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
            'P_value': f'{p}',
            'P-value rank': rank,
            'P-value Percentile': sig_p,
            'Effect_size': f'{e}',
            'Effect size upregulated rank': up_rank_es,
            'Effect size downregulated rank': down_rank_es,
            'Effect size percentile': sig_desc,
            'Effect size rank total': sig_desc_total,
        })

    if de_table:
        de_df = pd.DataFrame(de_table)
        de_df = de_df.set_index(['Study', 'Description', 'Condition'])
    else:
        de_df = pd.DataFrame(columns=['Study', 'Description', 'Condition'])
        de_df = de_df.set_index(['Study', 'Description', 'Condition'])

    
    ### Array ###
  
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

        # Rename Fold Difference to Fold Change if needed
        data.columns = data.columns.str.replace("Fold Difference", "Fold Change")

        data["Fold Change"] = pd.to_numeric(data["Fold Change"], errors="coerce")
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
            'Microarray Reference': f'{ref}',
            'Microarray Comparison': f'{comp}',
            'Microarray Reference (log2)': f'{ref_log}',
            'Microarray Comparison (log2)': f'{comp_log}',
            'Microarray Fold Change': f'{FC}',
            'Microarray Fold Change Up Rank': up_rank,
            'Microarray Fold Change Down Rank': down_rank,
            'Microarray Fold Change Percentile': sig_desc,
            'Microarray Fold Change Rank size': sig_desc_total,

        })
    if array_table:
        array_df = pd.DataFrame(array_table)
        array_df = array_df.set_index(['Study', 'Description', 'Condition'])
    else:
        array_df = pd.DataFrame(columns=['Study', 'Description', 'Condition'])
        array_df = array_df.set_index(['Study', 'Description', 'Condition'])

    
    ### Merge ###
   

    merged_df = results_df.merge(de_df, left_index=True, right_index=True, how="outer")
    merged_df2 = merged_df.merge(array_df, left_index=True, right_index=True, how="outer")


    ### Proteomics ###
    #####################

    ### Peptide Count ###
    gene_peptide_row = peptide_count[peptide_count["Gene ID"] == gene].copy()
    gene_peptide_row["Total number of samples"]=63

    if gene_peptide_row.empty:
        pep_long = pd.DataFrame([{
            "Metric": "Mass Spec Peptide Count",
            "Value": "No data available"
        }])

    else:
        gene_peptide_row = gene_peptide_row.drop(["Gene ID","source_id"], axis=1)
        pep_long = gene_peptide_row.melt(var_name='Metric', value_name='Value')
        pep_long['Data Type'] = 'Mass Spectrometry Peptide Counts'
    pep_long['Study'] = 'N/A'
    pep_long['Description'] = 'Peptide count data from Mass Spec experiments'
 
    pep_long['Condition'] = 'N/A'
    pep_long['Data Type'] = 'Mass Spectrometry Peptide Counts'
            


    ### DCC study ###
    dcc_table = []
    dcc_path = Path("DCC")

    for file_path in dcc_path.glob("*.txt"):
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

        p = gene_row["p value"].values[0]
        fc = gene_row["Fold Change"].values[0]

        # Fold change ranking
        upregulated_f = data[data["Fold Change"] > 0].copy()
        downregulated_f = data[data["Fold Change"] < 0].copy()
        no_change_f = data[data["Fold Change"] == 0].copy()

        upregulated_f["up_rank"] = upregulated_f["Fold Change"].rank(method="min", ascending=False)
        upregulated_f["percentile"] = (upregulated_f["up_rank"] / len(upregulated_f)) * 100

        downregulated_f["down_rank"] = downregulated_f["Fold Change"].rank(method="min", ascending=True)
        downregulated_f["percentile"] = (downregulated_f["down_rank"] / len(downregulated_f)) * 100

        no_change_f["up_rank"] = None
        no_change_f["down_rank"] = None
        no_change_f["percentile"] = None

        data_f = pd.concat([upregulated_f, downregulated_f, no_change_f]).sort_index()
        gene_row_f = data_f[data_f["Gene ID"] == gene]

        up_rank_f = None
        down_rank_f = None

        if fc > 0:
            up_rank_f = gene_row_f["up_rank"].values[0]
            percentile_f = gene_row_f["percentile"].values[0]
            sig_desc = f"Top {percentile_f:.1f}% of upregulated genes"
            sig_desc_total = len(upregulated_f)
        elif fc < 0:
            down_rank_f = gene_row_f["down_rank"].values[0]
            percentile_f = gene_row_f["percentile"].values[0]
            sig_desc = f"Top {percentile_f:.1f}% of downregulated genes"
            sig_desc_total = len(downregulated_f)
        else:
            sig_desc = "No change (Fold Change = 0)"
            sig_desc_total = len(no_change_f)

        # P-value ranking
        sigpval = data[data["p value"] < 0.05].copy()
        nonsigpval = data[data["p value"] >= 0.05].copy()

        sigpval["sig_rank"] = sigpval["p value"].rank(method="min", ascending=True)
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

        dcc_table.append({
            'Study': study_name,
            'Description': description,
            'Condition': comparison,
            'Quantitative Proteomics P_value': p,
            'Quantitative Proteomics P_value rank': rank,
            'Quantitative Proteomics P-value Percentile': sig_p,
            'Quantitative Proteomics Fold Change': fc,
            'Quantitative Proteomics Fold Change upregulated rank': up_rank_f,
            'Quantitative Proteomics Fold Change downregulated rank': down_rank_f,
            'Quantitative Proteomics Fold Change percentile': sig_desc,
            'Quantitative Proteomics Fold Change rank total': sig_desc_total,
        })

    if dcc_table:
        dcc_df = pd.DataFrame(dcc_table)
        dcc_df = dcc_df.set_index(['Study', 'Description', 'Condition'])
    else:
        dcc_df = pd.DataFrame(columns=['Study', 'Description', 'Condition'])
        dcc_df = dcc_df.set_index(['Study', 'Description', 'Condition'])
    ### FC studies ###
    fc_table = []
    folder_path = Path("FC")

    for file_path in folder_path.glob("*.txt"):
        with open(file_path, 'r') as f:
            study_name = f.readline().strip()
            description = f.readline().strip()
            comparison = f.readline().strip()

        data = pd.read_csv(file_path, sep="\t", skiprows=3)
        data.columns = data.columns.str.strip()
        total_genes = len(data)

        data["Fold Difference"] = pd.to_numeric(data["Fold Difference"])

        upregulated = data[data["Fold Difference"] > 0].copy()
        downregulated = data[data["Fold Difference"] < 0].copy()
        no_change = data[data["Fold Difference"] == 0].copy()

        upregulated["up_rank"] = upregulated["Fold Difference"].rank(method="min", ascending=False)
        upregulated["percentile"] = (upregulated["up_rank"] / len(upregulated)) * 100

        downregulated["down_rank"] = downregulated["Fold Difference"].rank(method="min", ascending=True)
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
        FC = gene_row["Fold Difference"].values[0]
        percentile = gene_row["percentile"].values[0]
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

        fc_table.append({
            'Study': study_name,
            'Description': description,
            'Condition': comparison,
            'Quantitiative Proteomics Reference': ref,
            "Quantitative Proteomics Comparison": comp,
            'Quantitative Proteomics Reference (log2)': ref_log,
            'Quantitative Proteomics (log2)': comp_log,
            'Quantitative Proteomics Fold Difference': FC,
            'Quantitative Proteomics Fold Difference Upregulated Rank': up_rank,
            'Quantitative Proteomics Fold Difference Downregulated Rank': down_rank,
            'Quantitative Proteomics Fold Difference Percentile ': sig_desc,
            'Quantitative Proteomics Fold Difference Rank Size': sig_desc_total,
        })

    if fc_table:
        fc_df = pd.DataFrame(fc_table)
        fc_df = fc_df.set_index(['Study', 'Description', 'Condition'])
    else:
        fc_df = pd.DataFrame(columns=['Study', 'Description', 'Condition'])
        fc_df = fc_df.set_index(['Study', 'Description', 'Condition'])



    ### Merge ###
    proteomics_df = dcc_df.merge(fc_df, left_index=True, right_index=True, how="outer")
    

    ### PTM ###
    ###########
    ptm_records = []
    for files in glob.glob("PTM/*.txt"):
        ptm_data = pd.read_csv(files, sep="\t")
        ptm_type = os.path.basename(files).replace(".txt", "")
        ptm_row = ptm_data[ptm_data["Gene ID"] == gene].copy()
        if ptm_row.empty:
            ptm_records.append({'Metric': ptm_type, 'Value': 'No data available'})
        else:
            ptm_site = ptm_row["Total Modifications By Type"].values[0]
            ptm_records.append({'Metric': ptm_type, 'Value': ptm_site})

    ptm_long = pd.DataFrame(ptm_records)
    ptm_long['Data Type'] = 'Post Translational Modification'
    ptm_long['Study'] = 'N/A'
    ptm_long['Description'] = 'N/A'
    ptm_long['Condition'] = 'N/A'
        
    
    ### Mutagenesis ###
    ###################
    piggybac=pd.read_csv("piggy.txt", sep="\t")
    gene_piggy_row = piggybac[piggybac["Gene ID"] == gene].copy()
    if gene_piggy_row.empty:
        mfs_long = pd.DataFrame([{'Metric': 'Mutant Fitness Score', 'Value': 'No data available'}])
    else:
        mfs = gene_piggy_row[["P.falciparum 3D7 piggyBac insertion mutagenesis - mutant fitness score"]]
        mfs_long = mfs.melt(var_name='Metric', value_name='Value')
        mfs_long['Data Type'] = 'Mutagenesis'
    mfs_long['Study'] = 'piggyBac insertion mutagenesis'
    mfs_long['Description'] = 'P. falciparum NF54 piggyBac mutagenesis'
    mfs_long['Condition'] = 'N/A'
    mfs_long['Data Type'] = 'Mutagenesis'

    ### Make table ###
    ##################
    os.makedirs(f"data_outputs/{gene}", exist_ok=True)
    # Transcriptomics
    trans_long = merged_df2.reset_index().melt(
        id_vars=['Study', 'Description', 'Condition'],
        var_name='Metric',
        value_name='Value'
    )
    trans_long['Data Type'] = 'Transcriptomics'

    # Proteomics
    prot_long = proteomics_df.reset_index().melt(
        id_vars=['Study', 'Description', 'Condition'],
        var_name='Metric',
        value_name='Value'
    )
    prot_long['Data Type'] = 'Quantitative Proteomics'
    

    # Concat
    final_df = pd.concat([prot_long, ptm_long, pep_long, mfs_long], ignore_index=True)
    final_df = final_df[['Data Type', 'Study', 'Description', 'Condition', 'Metric', 'Value']]
    #only want the descriptions for the studies once per occurence (looks for duplications)
    final_df = final_df.sort_values(['Data Type', 'Study', 'Condition']).reset_index(drop=True)
    final_df = final_df[
        final_df['Value'].notna() &
        (final_df['Value'] != '') &
        (final_df['Value'] != 'No data available')
    ]
    if final_df.empty:
        final_df = pd.DataFrame([{
            'Data Type': 'N/A',
            'Study': 'N/A',
            'Description': 'No data available for this gene',
            'Condition': 'N/A',
            'Metric': 'N/A',
            'Value': 'No data available',
        }])
    # after sorting
    merged_df2 = merged_df2.reset_index()
    merged_df2 = merged_df2.sort_values(['Study', 'Condition']).reset_index(drop=True)

    # only keep description on first occurrence of each study
    merged_df2['Description'] = merged_df2['Description'].where(
        ~merged_df2['Study'].duplicated(),
        other=''
    )
    if merged_df2.empty:
        merged_df2 = pd.DataFrame([{
            'Study': 'N/A',
            'Description': 'No transcriptomics data available',
            'Condition': 'N/A',
        }])
    merged_df2.to_csv(f"data_outputs/{gene}/transcriptomics.tsv", sep="\t", index=False)
    # after sorting
    final_df = final_df.sort_values(['Data Type', 'Study', 'Condition']).reset_index(drop=True)

    # only keep description on first occurrence of each study
    final_df['Description'] = final_df['Description'].where(
        ~final_df['Study'].duplicated(), 
        other=''
    )
    final_df.to_csv(f"data_outputs/{gene}/combined_prompt_data.tsv", sep="\t", index=False)

