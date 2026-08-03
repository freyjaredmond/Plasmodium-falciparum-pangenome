**Schizont-Peaking, Blood-Stage-Dominant Gene with Extreme Strain Variation and Epigenetic Regulation**

This gene in <i>Plasmodium falciparum</i> is among the most highly expressed during asexual blood stages, with a characteristic biphasic intraerythrocytic developmental cycle (IDC) pattern: high expression in early rings, a trophozoite-stage trough, and peak expression during schizogony.

- **Schizont-stage peak** is highly conserved across strains and platforms, with dramatic upregulation from mid-trophozoite to late trophozoite/schizont (FC 8.7, top 5.3%, p=4.8e-21 in one replicated study; FC 8.1, top 7.4%, p=2.7e-21 in another).
- **Blood-stage specificity**: expression is massively reduced in sporozoites versus blood stages (FC -219.5, top 0.3% downregulated, p=2.1e-13).
- **Extreme strain variation**: 3D7 expression is ~34-fold higher than HB3 (p=1.3e-43), suggesting variant gene family membership.
- **Epigenetic control**: strongly regulated by PfSir2A/B, with the most downregulated gene in sir2a KO rings.
- **Sexual commitment enrichment**: upregulated 3.7-fold (top 1.0%) in sexually committed schizonts, with sharp silencing during gametocyte maturation (FC -20.5 stage II-to-V) and male-enriched expression.
- **Translational regulation**: polysomal enrichment at trophozoite/schizont stages (FC 6.9, top 5.6%; p=1.2e-3).

This expression profile—schizont-specific, epigenetically regulated, strain-variable, and invasion-pathway-sensitive—is consistent with a role in merozoite biology or erythrocyte invasion.

## Key Experiments

### Intraerythrocytic Developmental Cycle Expression

Across multiple IDC time-course datasets, this gene consistently shows a biphasic pattern with ring-stage and schizont-stage peaks separated by a trophozoite trough. The trophozoite-to-schizont upregulation is highly significant (FC 8.7, p=4.8e-21; FC 8.1, p=2.7e-21), conserved across 3D7, DD2, and HB3 strains, and confirmed by polysomal enrichment at schizont stage (FC 5.8, top 7.0%).

- Blood stage transcriptome (3D7) (Otto et al.) (RNA-seq) | BI: 3 | C: N/A
  - Highly expressed at 0hr (rank 41, top 0.8%) with trophozoite-stage trough at 16hr (FC -4.0) and recovery by 40-48hr, indicating peak expression in early ring stages.
- Erythrocytic expression time series (3D7, DD2, HB3) (Bozdech et al. and Llinas et al.) (array) | BI: 5 | C: N/A
  - Consistent trophozoite downregulation followed by schizont upregulation across all three strains (e.g. DD2 FC 1.9, top 1.2%; HB3 FC 3.9, top 2.2%).
- High resolution intraerythrocytic time course transcriptome by RNA-Seq (Kucharski and Tripathi et al.) (RNA-seq) | BI: 2 | C: N/A
  - Well-expressed at 4hr (rank 133, top 2.5%) with trophozoite trough at 22-26hr and schizont recovery.
- IDC in constant temperature and darkness (2020) (Subudhi et al. 2020) (RNA-seq) | BI: 4 | C: N/A
  - Schizont-stage peak at 32hr (FC 43.5) under constant conditions, suggesting circadian-independent regulation.
- Intraerythrocytic development cycle transcriptome (2018) (Toenhake et al.) (RNA-seq) | BI: 4 | C: N/A
  - Classic biphasic pattern: ring peak (1024 TPM, rank 156, top 2.9%), trophozoite trough, and schizont recovery (FC 5.7).
- Intraerythrocytic development cycle transcriptome (2019) (Wichers et al. 2019) (RNA-seq) | BI: 5 | C: 5
  - Dramatic, highly significant upregulation from mid- to late trophozoite (FC 8.7, top 5.3%, p=4.8e-21, effect size 3.3).
- Strand specific transcriptome of the intraerythrocytic developmental cycle (Siegel et al.) (RNA-seq) | BI: 4 | C: N/A
  - Downregulated at 20-30hr, with strong upregulation at 40hr (FC 7.1 from 30hr, top 13.8%).
- Pfal3D7 real-time transcription and decay () | BI: 4 | C: N/A
  - Very high nascent transcript expression (rank 23, top 0.4%) with regulated mRNA stability during ring-to-trophozoite transition.
- Polysomal and steady-state asexual stage transcriptomes (Bunnik et al.) (RNA-seq) | BI: 5 | C: 2
  - Strong polysomal enrichment at trophozoite (FC 6.9, top 5.6%) and schizont (FC 5.8, top 7.0%) stages indicating active translation (p=1.2e-3).

### Strain Variation and Comparative Expression

This gene exhibits extreme inter-strain expression variation, with 3D7 expressing ~34-fold more than HB3 (p=1.3e-43), and field isolates showing ~5-fold lower expression than lab-adapted 3D7, pointing to potential variant gene family membership.

- Intraerythrocytic development cycle transcriptome by DAFT-Seq (3D7, HB3, IT, 2020) (Chappell et al. 2020) (RNA-seq) | BI: 5 | C: 5
  - Very highly expressed in 3D7 (2883 TPM, rank 15, top 0.3%) but dramatically downregulated in HB3 (FC -33.6, p=1.3e-43) and IT (FC -10.0, p=3.4e-16).
- NSR-seq Transcript Profiling of malaria-infected pregnant women and children (Vignali et al.) (RNA-seq) | BI: 5 | C: N/A
  - Highly expressed in field isolates (1353 TPM, rank 143) but ~5-fold lower than 3D7, with consistent expression between field pools.

### Life Cycle and Mosquito-Stage Expression

This gene is predominantly blood-stage-specific, with massive downregulation in sporozoites (FC -219.5, p=2.1e-13) and modest oocyst expression; modest upregulation in oocysts versus blood stages may relate to antisense regulation.

- Asexual blood stages, salivary gland sporozoite and midgut oocyst transcriptomes (Gomez-Diaz) (RNA-seq) | BI: 5 | C: 5
  - Upregulated in midgut oocysts versus blood stages (FC 1.3, top 8.8%, p=7.0e-8); antisense transcripts show stronger upregulation in oocysts (top 1.6%) and sporozoites (top 4.5%).
- Mosquito or cultured sporozoites and blood stage transcriptome (NF54) (Hoffmann et al.) (RNA-seq) | BI: 5 | C: 5
  - Massively downregulated in cultured sporozoites (FC -219.5, top 0.3%, p=2.1e-13) and mosquito sporozoites (FC -76.4, p=2.7e-7) versus blood stages (1977 TPM, rank 36).
- Transcriptome of the asexual life stages (Tang et al. 2020) (RNA-seq) | BI: 5 | C: 5
  - Strongly upregulated ring to schizont (sense FC 8.1, p=2.7e-21); significant downregulation sporozoite to trophozoite (p=3.0e-13).
- Ring, Oocyst and Sporozoite Transcriptomes (Zanghi et al.) (RNA-seq) | BI: 5 | C: 5
  - Significant oocyst-to-ring downregulation in sense (p=2.1e-19, effect size 4.7), confirming blood-stage dominance.
- Life cycle expression data (3D7) (Le Roch et al.) (array) | BI: 5 | C: N/A
  - Moderate-to-high expression across erythrocytic stages (top 0.3-1.8% rank) with progressive upregulation through schizogony.
- Comparison of in vitro versus aseptic mosquito produced sporozoites by RNA-seq (Eappen et al. 2022) (RNA-seq) | BI: 3 | C: N/A
  - Divergent sense (downregulated) and antisense (upregulated) expression between mosquito-produced and in vitro sporozoites.

### Sexual Stage and Gametocyte Expression

This gene is sharply upregulated during sexual commitment (FC 3.7, top 1.0% in committed schizonts), highly expressed in early gametocytes, then dramatically silenced during maturation (stage II-to-V FC -20.5, top 0.3%), with pronounced male-enriched expression (female vs male FC -11.4).

- Sexually vs asexually committed schizont transcriptional profiles (Pelle et al.) (array) | BI: 5 | C: N/A
  - Among the most upregulated genes in sexually committed versus asexually committed schizonts (FC 3.7, top 1.0%).
- Gametocyte Transcriptomes (Lasonder et al.) (RNA-seq) | BI: 5 | C: N/A
  - Strongly downregulated in female versus male gametocytes in both antisense (FC -19.6, top 2.7%) and sense (FC -11.4, top 11.3%).
- Gametocyte stages I-V transcriptomes (Young et al.) (array) | BI: 5 | C: N/A
  - Highly expressed overall (top 1.1%) with progressive downregulation in mature gametocytes (day 12 FC -2.8, top 5.2%).
- Gametocyte time course from commitment to maturity (van Biljon et al.) (array) | BI: 5 | C: N/A
  - Among the most highly expressed at pre-induction (rank 61, top 1.1%) with progressive downregulation reaching nadir at day 12 (FC -4.5, top 3.0%).
- Strand specific transcriptomes of 4 life cycle stages (Lopez-Barragan et al.) (RNA-seq) | BI: 5 | C: N/A
  - Exceptional gametocyte stage II-to-V downregulation in antisense (FC -39.4, top 0.1%) and sense (FC -12.3, top 0.5%).
- Transcriptomes of 7 sexual and asexual life stages (Lopez-Barragan et al.) (RNA-seq) | BI: 5 | C: N/A
  - Dramatic upregulation early trophozoite to late trophozoite (FC 21.3), strong schizont-to-gametocyte II induction (FC 33.7, top 4.2%), and exceptional gametocyte II-to-V downregulation (FC -20.5, top 0.3%).

### Epigenetic Regulation and Knockout Studies

This gene is among the most sensitive to epigenetic perturbation, being the top downregulated gene in sir2a KO rings (FC -2.7, rank 1) and strongly downregulated in sir2b KO trophozoites (FC -4.0, top 0.1%), with consistent downregulation across invasion-pathway knockouts.

- Two Sir2 KO lines expression profiling (array) | BI: 5 | C: N/A
  - Among the most highly expressed (top 0.04-0.75%) and the most downregulated gene in sir2a KO rings (FC -2.7, rank 1) and sir2b KO trophozoites (FC -4.0, top 0.1%).
- Invasion pathway knockouts (Stubbs et al.) (array) | BI: 5 | C: N/A
  - Consistently downregulated across multiple invasion-pathway KO lines, most notably EBA140 KO (FC -1.9, top 0.9%) and SIR2 KO at 24hr (FC -1.8, top 1.6%).
- Transcriptome of Bromodomain protein conditional knockouts over the IDC (Josling et al. 2015) (array) | BI: 4 | C: N/A
  - Modest upregulation upon PfBDP1 knockdown (FC 1.2, top 11.4%), suggesting mild repression by PfBDP1.
- Trophozoite and Schizont transcriptomes of PfBDP1HA (Josling et al 2015) (RNA-seq) | BI: 5 | C: 5
  - Strongly downregulated schizont to trophozoite in sense (FC -17.5, p=1.1e-18, effect size -4.2) and antisense (FC -16.7, p=1.1e-8), confirming robust schizont-specific expression.

### Clinical and Field Isolate Expression

In clinical malaria samples, this gene is consistently upregulated in uncomplicated malaria versus severe phenotypes, most strikingly versus cerebral malaria (antisense FC 11.3, top 0.1%, p=7.3e-3), potentially reflecting stage composition differences or parasite fitness.

- Dual transcriptomes of malaria-infected Gambian children (RNA-Seq) | BI: 5 | C: 3
  - Strongly upregulated in uncomplicated versus cerebral malaria (antisense FC 11.3, top 0.1%, p=7.3e-3) and versus hyperlactatemia (FC 6.8, top 0.1%, p=2.7e-2), with a notable sex-associated expression difference (p=7.6e-4).

### Drug Response and Cytoadherence

This gene responds to chloroquine treatment in a PfCRT-mutation-dependent manner and shows expression variation linked to cytoadherence phenotype, with enrichment in CD36-binding parasites.

- Three Isogenic Lines w/ CQ Treatment: expression profiles (Jiang et al.) (array) | BI: 5 | C: N/A
  - Downregulated upon chloroquine treatment in CQ-resistant 106/76I line (FC -1.2, top 2.1%) but not in the sensitive parent, suggesting PfCRT-mutation-dependent transcriptional response.
- Transcriptome of sequestration phenotypes (Kamaliddin et al) (RNA-seq) | BI: 5 | C: N/A
  - Upregulated in CD36-binding parasites versus ICAM1-binding (FC 4.1, top 5.4%) and HBEC-5i-binding (FC 4.1, top 1.8%) phenotypes.

### Other

- Heat shock response in sensitive mutants (LRR5, DHC) (Zhang et al. 2021) (RNA-seq) | BI: 5 | C: 0
  - Modest upregulation in ΔDHC (FC 1.9, top 7.9%) and ΔLRR5 (FC 1.5, top 30.3%) mutants, but none statistically significant (all p>0.05).
- Oocyst and salivary gland sporozoite transcriptome comparison in <i>P. falciparum</i> (Lindner et al.) (RNA-seq) | BI: 0 | C: 0
  - No significant change between oocysts and salivary gland sporozoites (FC -1.3, p=0.94).
- Intraerythrocytic development cycle transcriptome by UTR-Seq (2020) (Chappell et al. 2020) (RNA-seq) | BI: 0 | C: 5
  - Exceptionally highly expressed (6088 TPM, rank 6, top 0.1%) but essentially constitutive during blood stages; statistical significance reflects protocol power rather than biological variation.
- Transcriptome in severe vs uncomplicated malaria (Tonkin-Hill et al 2018) (RNA-seq) | BI: 5 | C: 0
  - Modest upregulation in severe versus uncomplicated malaria (antisense FC 3.0, top 4.7%) but not statistically significant (p=0.70).