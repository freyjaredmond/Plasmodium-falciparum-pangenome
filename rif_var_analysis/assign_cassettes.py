## The script used to assign domain cassettes to the extracted domain subtypes
## Cassette definitions were taken from the original VarDom paper
import pandas as pd
import glob
import os

# assign domains to their cassettes
cassette_table = {
    "DC2":  [{"DBLpam1"}, {"DBLpam2"}, {"CIDRpam"}, {"DBLpam3"}, {"DBLepam4"}, {"DBLepam5"}, {"DBLe10"}],
    "DC3":  [{"DBLa1.3"}, {"DBLe8"}],
    "DC1":  [{"DBLa1.1", "DBLa1.4"}, {"CIDRa1.2", "CIDRa1.3"}, {"DBLb1", "DBLb11"}, {"DBLg1", "DBLg15"}, {"DBLe1"}, {"DBLg8"}, {"DBLz1", "DBLz2"}, {"DBLe5"}],
    "DC5":  [{"DBLg12"}, {"DBLd5"}, {"CIDRb3", "CIDRb4"}, {"DBLb7", "DBLb9"}],
    "DC16": [{"DBLa1.5", "DBLa1.6"}, {"CIDRd"}],
    "DC13": [{"DBLa1.7"}, {"CIDRa1.4"}],
    "DC15": [{"DBLa1.2"}, {"CIDRa1.5"}],
    "DC11": [{"DBLa1.8"}, {"CIDRb2"}, {"DBLg7"}],
    "DC6":  [{"DBLg14"}, {"DBLz5"}, {"DBLe4"}],
    "DC7":  [{"DBLe2"}, {"DBLe7"}, {"DBLe3"}],
    "DC9":  [{"DBLg3"}, {"DBLz4"}],
    "DC10": [{"DBLz6"}, {"DBLe9"}],
    "DC12": [{"DBLz3"}, {"DBLe12"}],
    "DC8":  [{"DBLa2"}, {"CIDRa1.1"}],
    "DC14": [{"DBLa0.6"}, {"CIDRa3.1"}, {"DBLb5"}],
    "DC17": [{"CIDRa5"}, {"DBLb5"}],
    "DC22": [{"DBLa0.4", "DBLa0.18"}, {"CIDRa6"}, {"DBLb5"}],
    "DC21": [{"DBLa0.18", "DBLa0.21"}, {"CIDRa2.1"}, {"DBLb2"}],
    "DC18": [{"DBLa0.14"}, {"CIDRa4"}],
    "DC19": [{"DBLa0.16"}, {"CIDRa3.4"}],
    "DC20": [{"DBLa0.9"}, {"CIDRa2.7"}]
}

# function to map cassette to gene
def assign_cassette(gene_domains, cassette_table):
    assigned = []
    for cassette, required_sets in cassette_table.items():
        n = len(required_sets)  # length of consecutive that must match
        for i in range(len(gene_domains) - n + 1):  # uses a sliding window to ensure consecutive matches
            window = gene_domains[i:i+n]
            if all(any(domain.startswith(req) for req in required_set)  # some have more detailed subtype information than is necessary
                   for domain, required_set in zip(window, required_sets)):
                assigned.append(cassette)
                break
    return assigned if assigned else ["no_cassette"]

all_results = []
domain_files = glob.glob("GET_PANGENES_pseudo/Var_analysis/domain_matches/*matches.tsv")

# get cassette info
for match in domain_files:
    genome = os.path.basename(match).split("_")[0]
    match_data = pd.read_csv(match, sep="\t")
    for gene_id, group in match_data.groupby("gene_id"):
        domains = group["subtype"].to_list()
        cassettes = assign_cassette(domains, cassette_table)
        all_results.append({
            "Genome": genome,
            "Gene": gene_id,
            "Domains": "|".join(domains),
            "Cassette": "|".join(cassettes)
        })

df = pd.DataFrame(all_results)

# split into matches and no matches
df_matches = df[df["Cassette"] != "no_cassette"]
df_no_matches = df[df["Cassette"] == "no_cassette"]

print(f"Total genes: {len(df)}")
print(f"Cassette assigned: {len(df_matches)}")
print(f"No cassette: {len(df_no_matches)}")
print(f"\nCassette counts:\n{df['Cassette'].value_counts()}")

# check multiple cassette assignments
multiple_cassettes = df_matches[df_matches["Cassette"].str.contains("\|")]  # pipe to separate more than one cassette
print(f"\nGenes with multiple cassette assignments: {len(multiple_cassettes)}")
print(multiple_cassettes[["Genome", "Gene", "Domains", "Cassette"]].to_string())
print(multiple_cassettes["Cassette"].value_counts())

df.to_csv("GET_PANGENES_pseudo/Var_analysis/cassette_assignments_final.tsv", sep="\t", index=False)  # save

domain_combo = df_no_matches["Domains"].value_counts()
print((domain_combo).head(20))

# were all cassettes identified
df_one_cassette = df[~df["Cassette"].str.contains("\|")]
vc = df_one_cassette["Cassette"].value_counts()
print(len(vc))
print(vc)

#assign the cassette if present but domains if not
df = df[~df["Cassette"].isin(["DC2", "DC1", "DC3"])]
df["Assignment"] = df.apply(
    lambda row: row["Cassette"] if row["Cassette"] != "no_cassette" else row["Domains"],
    axis=1
)
print(df.head(20))

df.to_csv("GET_PANGENES_pseudo/Var_analysis/domain_matches/domain_assignemnts.tsv", sep="\t")
