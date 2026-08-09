## Predicted Functions

1. Mitochondrial protein involved in mitochondrial import or mitochondrial membrane organization
2. Component of a mitochondrial metabolic pathway, potentially linked to pyrimidine biosynthesis support
3. Mitochondrial carrier or transporter protein facilitating small molecule or protein translocation
4. Accessory factor in mitochondrial protein quality control or chaperone activity
5. Housekeeping protein with a role in general cellular metabolism during asexual blood stages

## Summary

This gene encodes a lowly expressed, likely mitochondrial protein of unknown function in <i>Plasmodium falciparum</i>. Coexpression analysis strongly implicates mitochondrial localization, as the majority of its top coexpressed partners are mitochondrial import components (TIM8, TIM9, TIM10, TIM16, TOM22), mitochondrial carriers, and enzymes of the pyrimidine biosynthesis pathway (dihydroorotate dehydrogenase, aspartate carbamoyltransferase, orotate phosphoribosyltransferase). The gene is dispensable under standard growth conditions (negative piggyBac fitness score), shows very low expression across blood stages, and displays notable upregulation in uncomplicated malaria and early ring/trophozoite stages.

## Evidence

**Transcriptomics:** The gene is consistently lowly expressed across the intraerythrocytic developmental cycle (IDC), with expression ranks typically in the bottom 5–10% (expression percentile ~90–96%, indicating low expression). During the IDC (Toenhake, Wichers, Kucharski datasets), modest upregulation is observed at the trophozoite-to-schizont transition (e.g., Toenhake T20: 25.6× fold change, top 1.8% upregulated; Wichers late trophozoite to early schizont: 4.6×, top 6.8% upregulated). In UTR-seq (Chappell), 0hr to 8hr shows 4.0× upregulation (top 0.4%), suggesting early ring-stage induction. In the Gambian children dual transcriptome study, the gene is significantly upregulated in uncomplicated malaria vs. cerebral malaria (FC 10.7×, top 2.0%; p=0.006, effect size top 1.1%), and in uncomplicated vs. cerebral+hyperlactatemia (FC 6.2×, top 2.5%; p=0.0001, effect size top 4.1%). In male vs. female gametocytes (Lasonder), it is downregulated 19-fold in females (top 6.4% downregulated), implying male-enriched expression. Across strains (DAFT-seq), 3D7 expression is significantly higher than IT (FC −20.6×, top 1.5% downregulated; p=7.4e-41) and HB3 (FC −7.6×, top 7.8% downregulated), indicating strain-variable expression. Antisense transcription is minimal and not informative.

**Additional Data (Proteomics, Mutagenesis, PTMs):** Mass spectrometry detected only 1 out of 63 samples with peptides (2 unique peptides total), consistent with low abundance or restricted expression. The piggyBac mutagenesis fitness score is −1.181, indicating that disruption of this gene is tolerated or mildly deleterious, suggesting it is not essential under standard in vitro asexual growth conditions.

**Coexpression (WGCNA):** The top 50 coexpressed genes are heavily enriched for mitochondrial functions. Key coexpressed partners include mitochondrial import machinery (TIM8, TIM9, TIM10, TIM16, TOM22), mitochondrial carriers, GrpE (mitochondrial co-chaperone), LETM1-like protein (mitochondrial inner membrane), and Hsp70/Hsp90 activators. The GO term "mitochondrion" is the second most frequent annotation (16/50 genes), and mitochondrial import-related terms (protein targeting to mitochondrion, protein insertion into mitochondrial inner membrane, TIM23 complex) are prominent. Additionally, three enzymes of de novo pyrimidine biosynthesis are coexpressed (dihydroorotate dehydrogenase, aspartate carbamoyltransferase, orotate phosphoribosyltransferase), a pathway that relies on mitochondrial electron transport. The most frequent GO term is "nucleus" (20/50), but this likely reflects annotation of conserved Plasmodium proteins with dual or ambiguous localization; the mitochondrial signal is more coherent and functionally interpretable.

**Localisation:** No hyperLOPIT localization data is available for this gene.

**Binding:** No gold standard interactions or above-threshold MapX interactions are available.

## Confidence

Confidence in the mitochondrial functional assignment is moderate. The strongest evidence comes from the highly coherent coexpression module enriched in mitochondrial import components and pyrimidine biosynthesis enzymes. Transcriptomics supports low-level, trophozoite/schizont-peaking expression consistent with mitochondrial activity during these stages. However, the absence of localization data, meaningful protein interaction data, and robust proteomic detection limits direct validation. The very low expression and minimal proteomic evidence could also reflect a highly stage-restricted or condition-specific role. The negative piggyBac score and strain-variable expression suggest the gene may be functionally redundant or context-dependent.

## Experimental Validation

To confirm mitochondrial localization, epitope tagging (e.g., HA or GFP fusion at the C-terminus) followed by immunofluorescence microscopy with MitoTracker co-staining would be informative. Conditional knockdown (e.g., using the glucosamine-inducible glmS ribozyme or TetR-DOZI system) during the trophozoite-to-schizont transition could reveal growth or metabolic phenotypes. Immunoprecipitation followed by mass spectrometry (IP-MS) would identify binding partners and confirm association with mitochondrial import complexes. Bioinformatically, signal peptide and transmembrane domain prediction tools (e.g., MitoProt, TargetP, TMHMM) should be applied to assess mitochondrial targeting sequences. Metabolomic profiling after knockdown could test links to pyrimidine biosynthesis.