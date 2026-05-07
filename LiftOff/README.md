# *Plasmodium falciparum* LiftOff Analysis

This repository contains the relevant scripts for running the LiftOff analysis of the 3D7 genome annotations to the 19 whole genome *P. falciparum* assemblies. The aim of this analysis was to determine whether the 19 non-reference *P. falciparum* genomes present in PlasmoDB required updating with the curated annotations of the 3D7 reference genome.

---

## Running LiftOff
LiftOff version 1.6.3 was run on the HPC using [`LiftOff SLURM`](LiftOff%20SLURM). The results of LiftOff can be found for each genome within their corresponding folders e.g. [`pf7G8`](pf7G8).

---

## LiftOff Analysis
Plots of the number of valid ORFs and gene coverage were generated using [`investigating ORFs and Coverage`](investigating%20ORFs%20and%20Coverage). The relevant plots can be found in each genome's folder e.g. [`pf7G8`](pf7G8).

---

## GffCompare
GffCompare version 0.12.10 was run on the HPC, comparing the original genome annotations to the lifted over 3D7 annotations. The SLURM script can be found here: [`GffCompare SLURM`](GffCompare%20SLURM). The results of GffCompare can be found within each genome's folder.

---

## GffCompare Analysis
The frequency of GffCompare tracking codes was plotted using [`Plotting tracking codes`](Plotting%20tracking%20codes). The frequency of tracking codes was explored for all gene annotations as well as for gene annotations with valid ORFs using [`Filtering for valid ORF=1`](Filtering%20for%20valid%20ORF%3D1). The results of this analysis can be found in [`Tracking_codes.tsv.tsv`](Tracking_codes.tsv.tsv) and [`Tracking_codes_orf1.tsv`](Tracking_codes_orf1.tsv).

---

## Protein Alignment
To characterise genes that were not receiving exact matches between the original and lifted over annotations, pairwise protein alignment was carried out to determine sequence similarity using [`Protein Sequence Analysis`](Protein%20Sequence%20Analysis). The results can be found in the [`Protein Comparison`](Protein%20Comparison) folder.
