# Generating the *Plasmodium falciparum* Pangenome Using the GET_PANGENES Pipeline

This repository contains the scripts and outputs for running the GET_PANGENES pipeline 
on 20 *P. falciparum* whole-genome assemblies to generate the *P. falciparum* pangenome. 

Thescripts and outputs for the improved pangenome built from 16 *P. falciparum* assemblies with
pseudogene inclusion is also provided. The exlcuded genomes:
- ML01 (mixed infection)
- TG01 (mixed infection)
- SD01 (large missassembly)
- NF135.C10 (admixed infection)
  
---

## Running GET_PANGENES
The SLURM script for running the 20 genoome GET_PANGENES pangenome can be found here: [`Running GET_PANGENES`](Running%20GET_PANGENES).
The gff helper script produced by Luc was modifed to include pseudogenes- this can be found here: 
Output, including the pangenome matrix and pangenome growth simulation results, can be 
found in [`20 genome GET_PANGENES_OUTPUT`](GET_PANGENES_OUTPUT) and here [`16 genome GET_PANGENES_OUTPUT`](GET_PANGENES_OUTPUT_16_PSEUDO).

---

## Quality Control
Quality metrics were generated using the bash script [`Run quality control`](Quality/Run%20quality%20control), 
with the resulting metrics file found at [`20 pangenome quality`](Quality/all_clusters_quality.txt) and [`16 pangenome quality`](Quality/all_clusters_quality_PSEUDO.txt)
Plots of quality metrics were produced using [`Quality/Quality.py`](Quality/Quality.py) 
and can be found in the [`Quality`](Quality) folder.

![](Quality/Max_distance.png)

A Python script is also provided that maps each genome against 3D7 to identify any 
structural abnormalities: [`Gene Locations.py`](Gene%20Locations.py)

![Chromosome Location](Quality/Chromosome_location.png)
---

## Pangenome Graphs
The pangenome occupancy bar chart was generated using [`Pangenome_occupancy_graph.py`](Pangenome_occupancy_graph.py).
The singleton count per genome was generated using [`Singletons_graph.py`](Singletons_graph.py).

Pangenome growth simulation graphs were produced using 
[`Produce_pangenome_growth`](Produce_pangenome_growth), with results found in for the 20 genome pangenome
[`Core simulation`](core_gene.tab_core_both.pdf) and 
[`Pangenome simulation`](pan_gene.tab_pan.pdf). For the 16 pangenome they are located [`Core simulation`](core_gene.tab_core_both_PSEUDO.pdf) and 
[`Pangenome simulation`](pan_gene.tab_pan_PSEUDO.pdf).

The POCS dendrogram and heatmap were produced using [`POCS_Dendrogram.py`](POCS_Dendrogram.py).

# 20 pangenome quality
To explore the distribution of singletons [`POCS_Dendrogram.py`](POCS_Dendrogram.py).


The results of all of these analyses can be found in this folder:
# 20 pangenome

#16 pangenome



![Singleton Counts](Singleton_16.png)

![POCS Heatmap](POCS_heatmap_16.png)



