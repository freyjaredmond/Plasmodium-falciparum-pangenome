# A script to get the value counts and product description for the WGCNA genes
import pandas as pd
import os

data=pd.read_csv("idc_af3_top50.tsv", sep="\t")
#build the gene list
genes=pd.read_csv("unknown_genes.tsv", sep="\t")
gene_list=genes["gene_id"].to_list()

#build go dict
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
    interactor_list=[]
    gene_data=data[data["gene"]==gene]
    if gene_data.empty:
        os.makedirs(f"data_outputs/{gene}", exist_ok=True)
        with open(f"data_outputs/{gene}/wgcna_data.txt", "w") as w:
            w.write("****************\n")
            w.write("Top 50 coexpressed genes product descriptions in descending order \n")
            w.write("No coexpression data available\n")
        continue
    for interactor in gene_data["correlated_gene"]:
        interactor_list.append(interactor)
    interactor_df=pd.DataFrame(interactor_list, columns=["Interactor"])
    interactor_df["Product Description"]=interactor_df["Interactor"].map(prod_dict)
    interactor_df["GO terms"]=interactor_df["Interactor"].map(go_dict)

    os.makedirs(f"data_outputs/{gene}", exist_ok=True)
    with open (f"data_outputs/{gene}/wgcna_data.txt", "w") as w:
        w.write("****************\n")
        w.write("Top 50 coexpressed genes product descriptions in descending order \n")
        for prodes in interactor_df["Product Description"]:
            w.write(f"{prodes} \n")

        go_list=[]
        for idx, rows in interactor_df.iterrows():
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
        w.write("\nTop 50 coexpressed genes GO terms \n")
        for term, count in vc.items():
            w.write(f"{term}\t{count}\n")
