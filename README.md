# P_falciparum-pangenome
The scripts used to build and explore the pangenome of Plasmodium falciparum using the GET_PANGENES pipeline
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
