import requests
import time
import pandas as pd
import os

uniprot=pd.read_csv("Best_uniprot_annotations", sep="\t")
uniprot_list=uniprot["UniProt_main"].tolist()

os.makedirs("non3d7_cif_files", exist_ok=True) #make empty dictionary
for id in uniprot_list:
    r = requests.get(f"https://alphafold.ebi.ac.uk/api/prediction/{id}") #request the id
    if r.status_code == 200:  # if successful
        cif_url = r.json()[0]["cifUrl"]  #find the cifurl link
        cif_data=requests.get(cif_url)
        with open(f"non3d7_cif_files/{id}.cif", "wb") as f:  # open a new file in the non3d7_cif folder
                                                          # have to write in binary
            f.write(cif_data.content)
    time.sleep(0.5)





