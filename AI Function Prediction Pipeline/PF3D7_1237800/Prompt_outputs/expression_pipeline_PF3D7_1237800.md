## Predicted Functions

1. Ribosomal protein or translation-associated factor involved in cytoplasmic protein synthesis during the ring and early trophozoite stages of the intraerythrocytic developmental cycle.
2. Structural component of the ribosome contributing to ribosome biogenesis and assembly.
3. RNA-binding protein involved in mRNA processing or translational regulation.
4. Essential housekeeping gene required for parasite growth and proliferation during blood-stage development.
5. Protein involved in translational quality control or ribosome-associated chaperone activity.

## Summary

This gene encodes a protein most likely functioning as a ribosomal component or translation-associated factor essential for blood-stage parasite development. Its transcriptomic profile shows peak expression during ring and early trophozoite stages (8–24 hpi), consistent with active translation machinery assembly. Strong coexpression with ribosomal proteins (both 40S and 60S subunits), translation elongation factors, and aminoacyl-tRNA ligases strongly supports a role in protein synthesis. The highly negative piggyBac mutagenesis fitness score (−2.692) indicates essentiality. Proteomic data confirms the protein is present during blood stages with higher abundance at the ring stage, declining into schizonts.

## Evidence

**Transcriptomics:** The gene shows moderate expression during blood stages (expression percentile ~30–45%), with a clear expression peak during early-to-mid trophozoite stages. In the Otto et al. time course, expression is highest at 8 hr (FC 2.6, top 2.2% of upregulated genes vs 0 hr) and 24 hr (FC 2.7), declining by 48 hr. Similarly, in the Kucharski time course, expression peaks at 26–29 hr (FC ~2.1–2.3) and drops sharply by 46 hr (FC −4.2, top 8.7% downregulated). The DAFT-seq data confirms significant upregulation at 8 and 16 hr across strains (p = 9.15×10⁻⁴ and 8.03×10⁻⁵). Expression is strongly downregulated in sporozoites relative to blood stages (FC −39.4 in Hoffmann et al.) and in schizonts relative to rings (FC −4.0 in Tang et al., p = 3.4×10⁻⁶). Gametocyte expression is moderate but lower. This ring/early-trophozoite peak pattern is characteristic of translational machinery genes.

**Coexpression:** The top 50 WGCNA coexpressed genes are overwhelmingly dominated by ribosomal proteins: sixteen 60S subunit proteins (L3, L4, L5, L6, L7, L11a, L14, L15, L18, L19, L21, L23, L37, L44, P0, L7-3) and seven 40S subunit proteins (S3A, S4, S6, S7, S9, S15, S27). Additionally, translation elongation factors (EF-1β, EF-1γ, EF-2), aminoacyl-tRNA ligases (threonine-tRNA, proline-tRNA), translation initiation factors (eIF-2B, eIF-3B), and chaperonin T-complex subunits are coexpressed. GO terms confirm: "structural constituent of ribosome" (22/50), "translation" (21/50), "cytosolic large ribosomal subunit" (16/50), "nucleus" (41/50), and "RNA binding" (27/50). This strongly indicates the gene functions in translation.

**Additional data (proteomics and mutagenesis):** Mass spectrometry detected the protein in 5 of 63 samples with 4 unique peptides, indicating modest but confirmed protein-level expression. Quantitative proteomics shows the protein is more abundant at ring stage (log2 = 4.52) than trophozoite (3.91) or schizont (3.46), with a −2.1-fold decrease ring-to-schizont (top 12.9% downregulated). The PfCRK4 study shows a 2.09-fold increase from 29 to 37 hpi. The piggyBac mutagenesis fitness score of −2.692 is strongly negative, indicating the gene is likely essential for blood-stage growth, consistent with core translation machinery.

**Binding (MAPX interactions):** MAPX identifies interactions with falcilysin (2 counts), translation initiation factor eIF-1A (2 counts), phenylalanine-tRNA ligase subunits (alpha and beta, 2 counts each), 60S ribosomal protein L31, valine-tRNA ligase, and eukaryotic peptide chain release factor. GO terms of interactors include "translation" (2), "translational initiation" (2), "tRNA aminoacylation" (1), "RNA binding" (6), and "cytosol" (5). The interaction with multiple translation-associated proteins further supports a role in the translation apparatus. The interaction with falcilysin (a metallopeptidase) and food vacuole proteins (hemoglobin catabolic process, 3) may reflect co-fractionation artifacts or indirect associations.

**Localisation:** No hyperLOPIT localisation data is available for this gene.

## Confidence

Confidence is **high** that this gene encodes a translation-associated or ribosomal protein. The convergence across coexpression (dominated by ribosomal and translation genes), transcriptomics (ring/early-trophozoite peak matching known ribosomal gene profiles), proteomics (ring-enriched protein declining into schizonts), essentiality (strongly negative piggyBac score), and MAPX interactions (translation factors, tRNA ligases) provides robust multi-omic support. The only limitation is the absence of localisation data and gold-standard binding partners, which prevents definitive subunit or complex assignment. The relatively low mass spectrometry detection (5/63 samples) could reflect low abundance or difficulty in peptide detection, but does not contradict the functional prediction.

## Experimental Validation

Conditional knockdown (e.g., using the glmS ribozyme or DD/Shield system) during the ring/trophozoite stages could confirm essentiality and phenotype. Polysome profiling followed by western blot would verify ribosomal association. Co-immunoprecipitation with tagged ribosomal subunit markers would confirm complex membership. Fluorescence microscopy with epitope-tagged constructs would determine cytoplasmic/ribosomal localisation. Bioinformatically, structural domain prediction (e.g., InterPro, HHpred) could identify ribosomal protein folds or RNA-binding domains, and reciprocal BLAST against characterized ribosomal proteins from other eukaryotes could assign a specific subunit identity.