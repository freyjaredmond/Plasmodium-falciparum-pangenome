## Takes the results of the BLAST analysis and finds the annotation of the BLAST hit from the normalised data
## gff. The query sequence must be contained in the subject's sequence and the subject must have the same major
## domain type that VarDom assigned for it to be considered a match

import pandas as pd

#add the col names back in
blast_results = pd.read_csv("GET_PANGENES_pseudo/Var_analysis/blast_results/GB4_domains_blast.txt", 
                             sep="\t", 
                             header=None,
                             names=["qseqid", "sseqid", "pident", "length", "mismatch", 
                                    "gapopen", "qstart", "qend", "sstart", "send", 
                                    "evalue", "bitscore"])

blast_results[["gene_id", "domain_type", "domain_count", "domain_start", "domain_end"]] = \
    blast_results["qseqid"].str.split("|", expand=True)  #extract the info needed

# remove duplicate for the same match
blast_results = blast_results.drop_duplicates(subset=["qseqid", "sseqid"], keep="first")
#read subtypes txt file from vardb
subtypes = pd.read_csv("GET_PANGENES_pseudo/Var_analysis/blast_results/varDB.Normalised.Subdomains.txt", sep="\t", header=None)
subtype_dict = dict(zip(subtypes[0], subtypes[1])) #make a dict
#read the subtypes gff
subtypes_gff = pd.read_csv("GET_PANGENES_pseudo/Var_analysis/blast_results/varDB.Normalised.Subdomains.gff", sep="\t", header=None)

def get_subtype_from_gff(row, gff, blast_df):
    query_hits = blast_df[blast_df["qseqid"] == row["qseqid"]] #xetract the query
    query_class = row["domain_type"]
    
    for _, hit in query_hits.iterrows():
        protein_hits = gff[gff[0] == hit["sseqid"]] #for every match get the gff coords
        match = protein_hits[
            (protein_hits[3].astype(int) <= hit["send"] * 3) & #gff is nt
            (protein_hits[4].astype(int) >= hit["sstart"] * 3)# check if the subject is contained in the query
        ]
        if len(match) == 1:
            subtype = match[8].str.split("-").str[0].str.replace("note=", "").values[0] #get the gene name
            if subtype.startswith(query_class): #if the subtype matches the class that vardom assigned the coords
                hit = hit.copy()
                hit["subtype"] = subtype
                return hit # want the hit that gave the match not just the top hit
        elif len(match) > 1:
            match = match.copy()
            match["subtype"] = match[8].str.split("-").str[0].str.replace("note=", "")
            class_match = match[match["subtype"].str.startswith(query_class)]
            if len(class_match) == 1: #only selects it if only one domain matches
                hit = hit.copy()
                hit["subtype"] = class_match["subtype"].values[0]
                return hit
    
    # just keeps the top hit but assigns the subtype as no confident macth 
    first_hit = query_hits.iloc[0].copy()
    first_hit["subtype"] = "no_confident_match"
    return first_hit

# get unique queries - only want to run once per query
unique_queries = blast_results.drop_duplicates(subset=["qseqid"], keep="first").copy()
results = unique_queries.apply(
    lambda row: get_subtype_from_gff(row, subtypes_gff, blast_results), axis=1 #apply across the rows
) 

problem_domains = results[results["subtype"] == "no_confident_match"].copy()
top_hits_good = results[results["subtype"] != "no_confident_match"].copy()

problem_domains.to_csv("GET_PANGENES_pseudo/Var_analysis/domain_matches/GB4_problem.tsv", sep="\t", index=False)
top_hits_good.to_csv("GET_PANGENES_pseudo/Var_analysis/domain_matches/GB4_matches.tsv", sep="\t", index=False)

print(f"Good matches: {len(top_hits_good)}")
print(f"Problem domains: {len(problem_domains)}")
