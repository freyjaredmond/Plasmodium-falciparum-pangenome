# A script that identifies the subcellular localisation and gets the go terms of the genes in that subcellular localisation- also identifies any wgcna genes in the same network
import pandas as pd
from pathlib import Path
import re
import os
import glob

#build the gene list
genes=pd.read_csv("unknown_genes.tsv", sep="\t")
gene_list=genes["gene_id"].to_list()

#build wgcna coexpression data
wgcna_data=pd.read_csv("idc_af3_top50.tsv", sep="\t")

#build go
go=pd.read_csv("Curated_GO_genes.tsv", sep="\t")
go_dict={}
for idx, row in go.iterrows():
    cc=row["Curated GO Components"]
    mf=row["Curated GO Functions"]
    bp=row["Curated GO Processes"]
    gene=row["Gene ID"]
    go_dict[gene]=[cc,mf,bp]
#build product description dict
prod=pd.read_csv("product_des.txt", sep="\t")
prod_dict=dict(zip(prod["Gene ID"],prod["Product Description"]))

for gene in gene_list:
    folder_path = Path("Location")
    found = False
    for file_path in folder_path.glob("*.txt"):
        data = pd.read_csv(file_path, sep="\t")
        location_list=data["Gene ID"].to_list()
        if gene in location_list:
            found = True
            location_data=data
            folder_name=os.path.basename(file_path)
            location=folder_name.replace(".txt","")
            location_data["GO terms"]=location_data["Gene ID"].map(go_dict)
            os.makedirs(f"data_outputs/{gene}", exist_ok=True)
            with open (f"data_outputs/{gene}/location_data.txt", "w") as w:
                w.write("****************\n")
                w.write("Subcellular localisation \n")
                w.write(f"{location}\n")
            
                go_list=[]
                for idx, rows in location_data.iterrows():
                    go_terms=rows["GO terms"]
                    if not isinstance(go_terms, list):
                        continue
                    for terms in go_terms:
                        if pd.isna(terms):
                            continue
                        for go_term in terms.replace("()","").split(";"):
                            go_term=go_term.strip()
                            if go_term:
                                go_list.append(go_term)
                vc=pd.Series(go_list).value_counts()
                vc=vc.head(50)
                w.write("****************\n")
                w.write("\nSubcellular localisation GO terms \n")
                for term, count in vc.items():
                    w.write(f"{term}\t{count}\n")
                wgcna_gene=wgcna_data[wgcna_data["gene"]==gene]
                interactor_list=wgcna_gene["correlated_gene"].to_list()
                same_interactor=set(location_list) & set(interactor_list)
                w.write("*********************\n")
                w.write("Coexpressed genes in the same subcellular localisation\n")
                for same in same_interactor:
                    same_prod=prod_dict.get(same, "No description available")
                    w.write(f"{same_prod}\n")

            break

    if not found:
        os.makedirs(f"data_outputs/{gene}", exist_ok=True)
        with open(f"data_outputs/{gene}/location_data.txt", "w") as w:
            w.write("****************\n")
            w.write("Subcellular localisation \n")
            w.write("No location data available\n")


