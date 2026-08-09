import pandas as pd
import os
#build the gene list
genes=pd.read_csv("unknown_genes.tsv", sep="\t")
gene_list=genes["gene_id"].to_list()

#build product description dict
prod=pd.read_csv("product_des.txt", sep="\t")
prod_dict=dict(zip(prod["Gene ID"],prod["Product Description"]))

go=pd.read_csv("Curated_GO_genes.tsv", sep="\t")
go_dict={}
for idx, row in go.iterrows():
    cc=row["Curated GO Components"]
    mf=row["Curated GO Functions"]
    bp=row["Curated GO Processes"]
    gene=row["Gene ID"]
    go_dict[gene]=[cc,mf,bp]

# get mapx binding data
gold=pd.read_csv("gold_standard.csv")
gold=gold[gold["complex"]==1]
threshold=pd.read_csv("mapx_pass_threshold.tsv", sep="\t")

def go_term_counts(df, top_n=50):
    go_list=[]
    for idx, row in df.iterrows():
        go_terms=row["GO terms"]
        if not isinstance(go_terms, list):
            continue
        for terms in go_terms:
            if pd.isna(terms):
                continue
            for go_term in terms.replace("()","").split(";"):
                go_term=go_term.strip()
                if go_term:
                    go_list.append(go_term)
    return pd.Series(go_list).value_counts().head(top_n)

for gene in gene_list:
    p1=gold[gold["protein1"]==gene].copy()
    p1["Interactor"]=p1["protein2"]
    p2=gold[gold["protein2"]==gene].copy()
    p2["Interactor"]=p2["protein1"]
    mapx=pd.concat([p1,p2])
    mapx["Gene of Interest"]=gene
    mapx["Product Description"]=mapx["Interactor"].map(prod_dict)
    mapx["GO terms"]=mapx["Interactor"].map(go_dict)
    with open(f"data_outputs/{gene}/mapx_data.txt","w") as w:
        w.write("Gold standard interactions \n")
        w.write("******************\n")
        if mapx.empty:
            w.write("No gold standard interactions available\n")
        else:
            prod_des_list=mapx["Product Description"].to_list()
            for des in prod_des_list:
                w.write(f"{des}\n")

        w.write("******************\n")
        w.write("Gold standard interactors GO term counts \n")
        if mapx.empty:
            w.write("No gold standard interactions available\n")
        else:
            gold_go_counts=go_term_counts(mapx)
            for term, count in gold_go_counts.items():
                w.write(f"{term}\t{count}\n")

        threshold_1=threshold[threshold["p1"]==gene].copy()
        threshold_1["Interactor"]=threshold_1["p2"]
        threshold_2=threshold[threshold["p2"]==gene].copy()
        threshold_2["Interactor"]=threshold_2["p1"]
        mapx_threshold=pd.concat([threshold_1,threshold_2])
        mapx_threshold["Gene of Interest"]=gene
        mapx_threshold["Product Description"]=mapx_threshold["Interactor"].map(prod_dict)
        mapx_threshold["GO terms"]=mapx_threshold["Interactor"].map(go_dict)

        #counts of interaction pairs
        w.write("******************\n")
        w.write("MapX interaction pair counts \n")
        if mapx_threshold.empty:
            w.write("No above-threshold MapX interactions available\n")
        else:
            pair_counts=mapx_threshold["Interactor"].value_counts()
            for interactor, count in pair_counts.items():
                desc=prod_dict.get(interactor, "No description available")
                w.write(f"{desc}\t{count}\n")

        w.write("******************\n")
        w.write("MapX above-threshold interactors GO term counts \n")
        if mapx_threshold.empty:
            w.write("No above-threshold MapX interactions available\n")
        else:
            threshold_go_counts=go_term_counts(mapx_threshold)
            for term, count in threshold_go_counts.items():
                w.write(f"{term}\t{count}\n")

        


