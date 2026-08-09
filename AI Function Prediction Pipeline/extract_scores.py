import pandas as pd
import glob
import os
import re
#extract gois and threshold status
data=pd.read_csv("wgcna_goi_gene_sequences.tsv", sep="\t")
data=data[["Gene of Interest","Gene","WGCNA source"]]

#create regexs for extracting the data from the jsons and for extracting interactions from folder names

chain_iptm_re = re.compile(r'"chain_iptm"\s*:\s*\[([^\]]*)\]')
actifptm_re = re.compile(r'"actifptm"\s*:\s*([0-9.eE+-]+)')
pair_folder_re = re.compile(r'^(pf3d7_\d+)_(pf3d7_\d+)$', re.IGNORECASE)

#get wgcna source for that gene
threshold_lookup = {
    (goi.upper(), interactor.upper()): status
    for goi, interactor, status in zip(data["Gene of Interest"], data["Gene"], data["WGCNA source"])
}

rows = []
for folder in glob.glob("af3_wgcna_output/*"):
    if not os.path.isdir(folder):
        continue
    folder_name = os.path.basename(folder)
    match = pair_folder_re.match(folder_name)
    if not match:
        continue
    goi, interactor = match.group(1).upper(), match.group(2).upper()

    chain_iptm = None
    actifptm = None
    for filepath in glob.glob(os.path.join(folder, "*.json")):
        name=os.path.basename(filepath)
        if ("summary_confidences") in name:
            with open (filepath,"r") as j:
                content = j.read()
                match = chain_iptm_re.search(content)
                chain_iptm = [float(x) for x in match.group(1).split(",")] if match else None

        if name=="results.json":
            with open (filepath,"r") as j:
                content= j.read()
                match = actifptm_re.search(content)
                actifptm = float(match.group(1)) if match else None

    rows.append({
        "Gene of Interest": goi,
        "Interactor": interactor,
        "Tag": threshold_lookup.get((goi, interactor)),
        "chain_iptm": chain_iptm,
        "actifptm": actifptm,
    })

results = pd.DataFrame(rows)

print(results.head())

results.to_csv("af3_wgcna_output/wgcna_scored.tsv", sep="\t")