## Predicted Functions

1. Subunit of the TRiC/CCT chaperonin complex (T-complex protein 1 subunit beta), involved in ATP-dependent protein folding in the cytosol.
2. Essential role in folding newly synthesized cytoskeletal proteins (actin, tubulin) and other substrates during intraerythrocytic development.
3. Contribution to proteostasis during trophozoite and early schizont stages, when translational demand is highest.
4. Participation in co-translational or post-translational folding of invasion-related and housekeeping proteins.
5. Potential moonlighting role in RNA-associated or nuclear processes, given nucleo-cytoplasmic localization.

## Summary

This gene encodes T-complex protein 1 subunit beta (CCT2/TCP-1β), a core component of the eukaryotic chaperonin TRiC/CCT complex. All seven other CCT subunits are confirmed gold-standard interactors, and MAP-X data recapitulates these interactions with high frequency. Coexpression with ribosomal proteins and translation factors indicates coordinated function during peak protein synthesis in trophozoites. The strongly negative piggyBac fitness score (−2.7) confirms essentiality in blood-stage growth, consistent with an indispensable role in cytosolic protein folding.

## Evidence

**Transcriptomics:** Expression peaks during the trophozoite stage (~16–24 hpi), with fold changes of 4–24× relative to early ring across multiple IDC RNA-seq datasets (rows 108–113, Toenhake; rows 129–130, Chappell DAFT-seq). Expression declines sharply at late schizont/merozoite stages (−5 to −8 fold at 40–48 hpi). This profile matches trophozoite-enriched chaperones needed for high translational throughput. A significant downregulation from mid-trophozoite to late trophozoite (row 121, p = 1.1 × 10⁻²¹, effect size top 2.9%) and from late trophozoite to early schizont (row 120, p = 6.8 × 10⁻⁵) confirms stage-specific regulation. In the oocyst-to-sporozoite transition, expression drops dramatically (−10.7 fold, row 5; −68 fold antisense, row 198), suggesting blood-stage–biased function.

**Coexpression (WGCNA):** The top 50 coexpressed genes are overwhelmingly ribosomal proteins (21 genes annotated "structural constituent of ribosome") and translation factors (elongation factors 1-alpha, 1-gamma, EF-2, eRF3). The dominant GO terms are translation (23), RNA binding (23), nucleus (41), and cytosol (12). Notably, two other CCT subunits (TCPγ, TCPζ) are among the coexpressed genes, strongly supporting identification as a CCT subunit. Chaperone-related terms (protein folding: 5; unfolded protein binding: 4; chaperonin-containing T-complex: 2) further support this assignment.

**Localization (hyperLOPIT):** Classified as nucleo-cytoplasm, consistent with the known dual localization of TRiC/CCT complex subunits. The niche GO terms include chaperonin-containing T-complex (8), unfolded protein binding (17), protein folding (17), and cytosol (28). Six coexpressed genes (HSP70, TCPζ, TCPγ, Obg-like ATPase 1, EF-2, eRF3) co-localize to this niche, reinforcing a shared functional context in cytosolic protein quality control.

**Binding (Gold standard and MAP-X):** All seven other TRiC/CCT subunits (α, γ, δ, ε, ζ, η, θ) are gold-standard interactors—the definitive signature of CCT subunit β. MAP-X data independently identifies interactions with each of these subunits at high recurrence (5–7 times across conditions). Additional MAP-X interactors include translation-related proteins (EF-2, lysine-tRNA ligase, eRF3) and metabolic enzymes (phosphofructokinase, aminopeptidases), representing likely folding substrates or transient associations.

**Proteomics (Additional data):** Detected in 32 of 63 mass spectrometry samples with 69 unique peptides (492 summed), indicating robust and widespread protein expression. Quantitative proteomics shows slight downregulation from ring to trophozoite (−1.4 fold) and ring to schizont (−1.5 fold), suggesting relatively stable protein levels across the IDC despite mRNA fluctuations—consistent with the long half-life expected for a stable complex subunit. The piggyBac mutant fitness score of −2.7 indicates the gene is essential for asexual blood-stage growth.

## Confidence

Confidence is very high. The convergence across all data types is exceptionally strong: (1) gold-standard protein interactions unambiguously identify this as CCT subunit β; (2) coexpression with other CCT subunits and ribosomal/translation machinery is entirely consistent; (3) localization to the nucleo-cytoplasm matches known CCT biology; (4) the transcriptomic profile (trophozoite-peaking, translation-correlated) is expected for a chaperonin; and (5) essentiality is confirmed by piggyBac mutagenesis. No contradictions are observed across data types. The only minor uncertainty is in potential additional functions (e.g., nuclear roles), which remain speculative.

## Experimental Validation

Conditional knockdown (e.g., using the glmS ribozyme or DD/Shield system) during the IDC would confirm the expected growth and invasion defect, particularly at trophozoite-to-schizont transition. Co-immunoprecipitation followed by mass spectrometry of the tagged protein would confirm the octameric TRiC complex composition. Substrate trapping experiments (using ATPase-dead mutants) could identify specific folding clients in <i>P. falciparum</i>. Fluorescence microscopy of an epitope-tagged allele would validate the nucleo-cytoplasmic localization predicted by hyperLOPIT. Bioinformatically, reciprocal BLAST and hidden Markov model searches against known CCT2/TCP-1β sequences from other eukaryotes would confirm orthology.