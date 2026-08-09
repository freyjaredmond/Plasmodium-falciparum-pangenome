# Construction of the Plasmodium falciparum Pangenome and AI-Based Functional Annotation
The scripts used to construct and analysis the pangenome of *Plasmodium falciparum*, as well
as the AI-based functional prediction of unknown *P. falciparum* genes.

# *P. falciparum* pangenome
----------------------------
## LiftOff Analysis
Prior to pangenome construction, LiftOff version 1.6.3 was used to transfer the curated 
gene annotations of the 3D7 reference genome to the 19 non-reference *P. falciparum* 
assemblies. This was performed as a quality check to assess whether the existing genome 
annotations required updating before inclusion in the pangenome. GffCompare version 0.12.10 
was used to compare the lifted over annotations to the original genome annotations, and 
pairwise protein alignment was carried out to characterise any non-exact matches. Only 
limited differences were identified and the original annotations were retained for 
pangenome construction.

Full details of the LiftOff analysis, including scripts and results, can be found in the
[LiftOff README](LiftOff/README.md).

----------------------------
## Running GET_PANGENES to Produce the *P. falciparum* Pangenome

To construct the *P. falciparum* pangenome, the GET_PANGENES pipeline was run on 20 
whole-genome *P. falciparum* assemblies.
Full details of the pipeline, scripts and 
outputs can be found in the [GET_PANGENES README](GET_PANGENES/README.md).

![Pangenome Occupancy](GET_PANGENES/Pangenome_occupancy_bar_growth.png)

----------------------------
## Rerunning GET_PANGENES
The analysis was re run on 16 genomes excluding ML01, TG01, SD01 and NF135.C10 were not found to be of high enough quality (mixed infections, assembly errors).These genomes were inflating the cloud, shell and soft-core count. Pseudogenes were also included to
promote pangenome completeness.
The below panel highlights the issues with the 20 genome pangenome
![20_pangenome](GET_PANGENES/20_genome_quality.png).

The results and scripts of the higher quality 16 genome pangenome are also found in [GET_PANGENES README](GET_PANGENES/README.md).

![16 genome](GET_PANGENES/16_genome.png)

----------------------------
## Analysing the pangenome

The mean percentage of pangenes with InterPro IDs, protein length, paralog count and ortholog count were mapped to the pangenome.
All of the scripts and analyses are found here [Exploring the pangenome README](Exploring_the_pangenome/README.md)

![Characterising the pangenome](Exploring_the_pangenome/Figure2_pangenome_characteristics_sixteen_PSEUDO.png)

----------------------------
## Evidence for pangenes
Mean pLDDT scores, RNA-seq data and peptide counts were mapped to the pangenome.
All of the scripts and analyses are found here [Exploring the pangenome README](Exploring_the_pangenome/README.md)

![Evidence for the pangenome](Exploring_the_pangenome/Figure3_pangenome_support_PSEUDO.png)

----------------------------
## Characterising the functions of pangenes
GO enrichment analysis was performed on the cloud and core genes. The scripts and outputs are found here: [README.md](Function_of_pangenes/README.md)

The representative InterPro domain was also assigned to each cluster and the percentage occupancy of that domain across the cluster was calculated. Selected families were explored as a case study to compare core vs host interaction associated domains
![Function of pangenes](Function_of_pangenes/Figure4_GO_sixteen.png)

----------------------------
## 
