## Extract the sequence for all the domains assigned by VarDom for downstream BLAST
## Must already have the co-ordinates from VarDom (can run on their server)
import pandas as pd
import glob
import os

fasta_files=glob.glob("GET_PANGENES_pseudo/Var_analysis/var_fasta/*.fasta")
coord_files=glob.glob("GET_PANGENES_pseudo/Var_analysis/domain_coords_no_cut/*.seqIdKeys")


### create a table with the gene and its domain type and coords
def parse_vardom(coord_file):
    lookup = []
    current_gene = None
    
    with open(coord_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(">"):
                current_gene = line.replace(">", "")
                parts = line.split("\t")
                if len(parts) == 5:
                    domain_type = parts[0]
                    start = int(parts[1])
                    end = int(parts[2])
                    score = parts[3]
                    evalue = parts[4]
                    lookup.append({
                        "gene_id": current_gene,
                        "domain_type": domain_type,
                        "start": start,
                        "end": end,
                        "score": score,
                        "evalue": evalue
                    })
    return lookup
# carry out for every genome
all_domains=[]
for files in coord_files:
    result=parse_vardom(files)
    all_domains.extend(result)

lookup_table=pd.DataFrame(all_domains)   
print(lookup_table.head())

## filter the fasta files using the coords to get the sequences for downstream BLAST

def extract_domains(fasta):
    genome = os.path.basename(fasta).replace("_var.fasta", "")
    sequences = {}
    current_id = None
    current_seq = []

    with open(fasta, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_id:
                    sequences[current_id] = "".join(current_seq) #joins the seq lines together
                current_id = line.replace(">", "")
                current_seq = []
            else:
                current_seq.append(line) #if not a header must be seq
        if current_id:
            sequences[current_id] = "".join(current_seq) #capture the last gene

    out_path = f"GET_PANGENES_pseudo/Var_analysis/domain_fasta_no_cut/{genome}_domains.fasta"
    with open(out_path, "w") as out:
        for gene_id, seq in sequences.items(): 
            gene_domains = lookup_table[lookup_table["gene_id"] == gene_id] #get all rows for that gene id
            domain_type_counts = {}
            for _, row in gene_domains.iterrows():
                domain_type = row["domain_type"]
                domain_type_counts[domain_type] = domain_type_counts.get(domain_type, 0) + 1 #get a count where there are multiple of the same domain type
                count = domain_type_counts[domain_type]
                header = f">{gene_id}|{domain_type}|{count}|{row['start']}|{row['end']}" #make the fasta header informative
                domain_seq = seq[row["start"]-1:row["end"]] #remember python indexinh
                out.write(header + "\n")
                out.write(domain_seq + "\n")
    
    print(f"{genome}: done")

for file in fasta_files:
    extract_domains(file)

result = parse_vardom("GET_PANGENES_pseudo/Var_analysis/domain_coords_no_cut/3D7.seqIdKeys")
