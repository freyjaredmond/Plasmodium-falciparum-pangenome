# Characterising *rif* and *var* genes across the *P.falciparum* pangenome

## *rif* analysis

*rif* subtypes were assigned using STRIDE with the output being listed in this folder [rif results](rif_results).
FHEYDER motifs were identified using exact string matching [rif_analysis.py](rif_analysis.py).

## *var* analysis
*var* domain types were assigned using VarDom, with the output being listed here [var_domain_coords](var_domain_coords).
The corresponding sequences for these domain coordinates where extracted using [domain_filter.py](domain_filter.py).
BLAST was then run on these sequence against a normalised dataset of *var* sequences, taken from https://pubmed.ncbi.nlm.nih.gov/32055709/
using the script [BLAST.txt](BLAST.txt) and the results are here [blast_results](blast_results).
Domain cassettes were assigned using [assign_cassettes.py](assign_cassettes.py).

## Visualisation
The *rif* and *var* panel was plotted using [panel_RIF.py](panel_RIF.py).
![RIF_Panel](panel_rif_var.png)
