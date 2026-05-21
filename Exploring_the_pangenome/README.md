# Exploring the pangenome
Here are the scripts and outputs of analysis used to explore the *P. falciparum* pangenome.

## Percentage with valid interpro domain
The interpro ids were taken from PlasmoDB and mapped to the pangene clusters, the mean percentage of pangenes within
each occupancy was calculated. [Interpro][valid_interpro.py]

## Protein length

The length of proteins were taken from PlasmoDB and mapped to the pangene clusters, a box plot was created to show
the distribution of protein lengths amongst pangenome classifications. [Protein length][protein_length.py]

## Paralog counts

The paralog counts were taken from PlasmoDB and mapped to the pangene clusters, a box plot was created to show
the distribution of paralog counts. [Paralog counts][paralog_count.py]. This analysis was also repeated with
RIF and VAR genes removed.

#Ortholog counts

The ortholog counts were taken from PlasmoDB and mapped to the pangene clusters, a box plot was created to show
the distribution of ortholog counts. This analysis was also repeated with
RIF and VAR genes removed.

