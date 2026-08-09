## Predicted Functions

1. Structural component of the cytoplasmic 40S ribosomal small subunit, functioning in mRNA translation during the intraerythrocytic developmental cycle.
2. Essential housekeeping ribosomal protein required for general protein synthesis throughout blood-stage parasite development.
3. Contributor to translational regulation, with peak expression during ring and trophozoite stages and declining expression during schizogony and late stages.
4. Participant in ribosome biogenesis and assembly within the nucleus before export to the cytoplasm.
5. Potential role in translational control during life-cycle stage transitions, including sexual and mosquito-stage development.

## Summary

This gene encodes a 40S ribosomal protein subunit that is an essential structural component of the small ribosomal subunit in <i>Plasmodium falciparum</i>. It is highly expressed during asexual blood stages, peaking during ring-to-trophozoite transition and declining at schizont stages. Its essentiality is confirmed by a strongly negative piggyBac fitness score (−2.415). The protein is abundant in mass spectrometry data, localises to the nucleus (consistent with ribosome assembly), physically interacts with dozens of other ribosomal proteins, and is coexpressed with translation machinery genes.

## Evidence

**Transcriptomics:** The gene is highly expressed during asexual blood stages, consistently ranking in the top 1–3% of expressed genes (e.g., TPM ~718–3586 at ring/0hr, expression rank 29–138). During the IDC time course, expression peaks at ring-to-trophozoite stages (0–24 hpi) and declines at schizont stages (40–48 hpi), with fold changes of −2.6 to −26.8 at late time points relative to 0hr (rows 9–10, 97–98). Microarray data corroborate this: expression drops at 31–48hr in 3D7, DD2, and HB3 (top 1.5–3.6% downregulated, rows 37–38, 46, 50). The gene is downregulated in sporozoites relative to blood stages (FC −4.4, row 3; −19.3 in cultured sporozoites, row 162), and in oocysts relative to rings. In gametocyte time courses, expression is relatively stable. Late trophozoite-to-early schizont transitions show significant downregulation (p=9.1e-5, top 5.3% effect size downregulated, row 120; p=4.9e-12, top 8.1% effect size downregulated, row 121). Antisense transcription is low but shows some variability across stages.

**Additional Data (Proteomics, Mutagenesis, PTMs):** The protein is robustly detected by mass spectrometry (27/63 samples positive, 53 unique peptides, 251 summed peptide counts), indicating high abundance. Quantitative proteomics shows moderate downregulation from ring to schizont (fold difference −1.4, top 46.8% downregulated), consistent with transcriptomic decline at late stages. The piggyBac mutagenesis fitness score of −2.415 indicates the gene is essential for blood-stage growth. Three phosphorylation sites suggest post-translational regulation. The protein was not enriched in apicoplast or ER fractions.

**Coexpression:** The top 50 WGCNA coexpressed genes are overwhelmingly ribosomal proteins (both 40S and 60S subunits) and translation factors (eIF3 subunits, elongation factor 1-gamma, aminoacyl-tRNA ligases, T-complex chaperonins). The dominant GO terms are "structural constituent of ribosome" (19 genes), "translation" (18), "cytosolic small ribosomal subunit" (12), "cytosolic large ribosomal subunit" (8), and "nucleus" (39). This strongly supports a core translation/ribosome function.

**Localisation:** The protein was classified into the "nucleus1" compartment by hyperLOPIT, consistent with ribosome assembly in the nucleolus before cytoplasmic export. Coexpressed genes in the same niche include RNA cytosine C(5)-methyltransferase and DNA/RNA-binding protein Alba 3, both nuclear RNA-processing factors. The GO terms for this niche are enriched for RNA binding, mRNA splicing, and rRNA processing, all consistent with ribosomal biogenesis.

**Binding:** Gold standard interactions comprise the complete set of ~72 ribosomal proteins (both 40S and 60S subunits), confirming this protein is a bona fide ribosome component. MAPX data independently recover nearly all these same ribosomal proteins with high recurrence (up to 7 independent identifications), with dominant GO terms being "structural constituent of ribosome" (233), "translation" (219), and "cytosolic large/small ribosomal subunit" (138/116). A few non-ribosomal MAPX hits (e.g., prefoldin, translation initiation factors) further support roles in ribosome assembly and translation.

## Confidence

Confidence is very high. All five data types converge on the same conclusion: this gene encodes an essential 40S ribosomal protein. The coexpression, binding, proteomics, and transcriptomics data are internally consistent and mutually reinforcing. The nuclear localisation is expected for a ribosomal protein undergoing assembly. The strongly negative piggyBac fitness score confirms essentiality. There are no contradictions across data types. The only minor caveat is that the specific 40S subunit identity (e.g., S2, S13, S14, etc.) cannot be definitively assigned from these data alone, but the functional assignment as a small ribosomal subunit protein is unambiguous.

## Experimental Validation

The ribosomal protein identity could be confirmed bioinformatically by BLAST or HMM searches of the protein sequence against known eukaryotic ribosomal protein families. Experimentally, epitope tagging (e.g., HA or GFP) followed by immunofluorescence microscopy would confirm nucleolar and cytoplasmic localisation. Co-immunoprecipitation followed by mass spectrometry would validate the interaction with other ribosomal subunits. Conditional knockdown (e.g., using the glmS ribozyme or DD/Shield system) with polysome profiling would confirm the requirement for functional ribosome assembly and translation. Sucrose gradient fractionation would verify incorporation into 40S subunits and 80S monosomes.