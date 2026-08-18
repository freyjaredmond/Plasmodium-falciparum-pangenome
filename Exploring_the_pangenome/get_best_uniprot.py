import requests #send http requests
import time #put a time delay on requests
import pandas as pd
df_non3d7=pd.read_csv("Functional_analysis/No_3D7_uni", sep="\t")
#make a function for getting the best uniprot id
def get_best_uniprot(gene_id):
    try:# doesnt crash if fails
        r = requests.get(                                    # sends a GET request to UniProt
        "https://rest.uniprot.org/uniprotkb/search",     
        params={
            "query": f"{gene_id} AND organism_id:5833",  # search for your gene ID in all P. falciparum isolates
            "fields": "accession,reviewed,annotation_score", # only return these columns
            "format": "json"})    #common format 
    #all the params are appended to the end of the https to get the required fields

        results = r.json()["results"]                  # extract the list of results
        reviewed = [x for x in results                 # filter for swiss prot
                    if x["entryType"] == "UniProtKB reviewed (Swiss-Prot)"]
        if reviewed:                                   # if any reviewed results exist
            return reviewed[0]["primaryAccession"]     # return first reviewed result 
        return results[0]["primaryAccession"]          #return the first result if not reviewed
    except:         # else return first unreviewed result
        return None 
    
df_non3d7["UniProt_main"] = None         #create a column for the new uniprot ids

for gene_id in df_non3d7["Gene_ID"]:                 
    uid = get_best_uniprot(gene_id)                  
    df_non3d7.loc[df_non3d7["Gene_ID"] == gene_id, "UniProt_main"] = uid  #assign the uniprot id 
    time.sleep(0.5)                                  # wait to not get blocked

df_non3d7.to_csv("Best_uniprot_annotations",sep="\t")
   