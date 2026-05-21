# Exploring the pangenome
Here are the scripts and outputs of analysis used to explore the *P. falciparum* pangenome, exploring interpro domains, paralog counts, ortholog counts and protein lengths.

## Percentage with valid InterPro domain
The InterPro IDs were taken from PlasmoDB and mapped to the pangene clusters, the mean percentage of pangenes within each occupancy was calculated. [InterPro](valid_interpro.py)

## Protein length
The length of proteins were taken from PlasmoDB and mapped to the pangene clusters, a box plot was created to show the distribution of protein lengths amongst pangenome classifications. [Protein length](protein_length.py)

## Paralog counts
The paralog counts were taken from PlasmoDB and mapped to the pangene clusters, a box plot was created to show the distribution of paralog counts. [Paralog counts](paralog_count.py). This analysis was also repeated with RIF and VAR genes removed. [Filtered Paralogs](paralog_box_filtered_sixteen.png)

## Ortholog counts
The ortholog counts were taken from PlasmoDB and mapped to the pangene clusters, a box plot was created to show the distribution of ortholog counts. This analysis was also repeated with RIF and VAR genes removed. [Filtered Orthologs](ortholog_box_filtered_sixteen.png)

![Pangenome characterisation](Figure2_pangenome_characterisation_sixteen.png)
