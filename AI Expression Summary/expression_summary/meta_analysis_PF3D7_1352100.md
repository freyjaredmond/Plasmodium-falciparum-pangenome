**Schizont-enriched blood-stage gene with downregulation in sporozoites and dynamic antisense regulation**

This gene in <i>Plasmodium falciparum</i> is predominantly expressed during the schizont stage of the intraerythrocytic developmental cycle (IDC) and is strongly downregulated in sporozoites relative to blood stages.

- **Schizont-stage peak expression** is consistently observed across multiple IDC datasets, with significant upregulation in schizonts versus rings (FC 3.0, p=6.2e-5) and significant downregulation at 32hr across multiple strains (FC -2.1, p=3.9e-10).
- **Strong downregulation in sporozoites** compared to blood stages (FC -45.7, p=6.3e-6 for mosquito sporozoites; FC -12.6, p=0.044 for cultured sporozoites), and further decline from oocyst to salivary gland sporozoite (FC -8.2, p=1.2e-7).
- **Upregulation in sexually committed schizonts** (FC 1.8, top 8.9%) and progressive downregulation after gametocyte induction (FC -2.2 by day 6).
- **Antisense transcription** peaks at late IDC time points (FC 6.1–7.3, top 5–16%) and shows notable upregulation in heat-shock-sensitive mutants.

These patterns suggest a role in schizont-stage biology, potentially linked to merozoite formation or invasion processes.

## Key Experiments

### Intraerythrocytic Development Cycle Expression

Multiple IDC studies converge on schizont-enriched expression with mid-cycle suppression. The DAFT-seq multi-strain dataset provides the strongest statistical support for downregulation at 32hr (FC -2.1, p=3.9e-10), while Tang et al. confirm significant schizont versus ring upregulation (FC 3.0, p=6.2e-5). Antisense transcripts peak at late time points (FC 6.1–7.3 at 35–40hr in Toenhake et al.).

- Blood stage transcriptome (3D7) (Otto et al.) (RNA-seq) | BI: 4 | C: DE not available
  - Peaks at 8hr (FC 1.8 vs 0hr, top 13.6% upregulated) and most downregulated at 32hr (FC -3.3, top 24.4% downregulated), suggesting early ring-stage enriched expression with reduced levels at trophozoite stages.
- Erythrocytic expression time series (3D7, DD2, HB3) (Bozdech et al. and Llinas et al.) (array) | BI: 5 | C: DE not available
  - Lowly expressed across all three strains with modest periodic changes and downregulation at mid-cycle time windows.
- Intraerythrocytic development cycle transcriptome (2018) (Toenhake et al.) (RNA-seq) | BI: 5 | C: DE not available
  - Antisense transcription peaks strongly at late time points (T35: FC 6.1, top 5.4%; T40: FC 7.3, top 15.5%) with divergent sense and antisense regulation.
- Intraerythrocytic development cycle transcriptome (2019) (Wichers et al. 2019) (RNA-seq) | BI: 3 | C: 1
  - Gradual increase from early ring to schizont stages (late ring FC 1.7, p=0.017) with trophozoite-stage decline.
- Intraerythrocytic development cycle transcriptome by DAFT-Seq (3D7, HB3, IT, 2020) (Chappell et al. 2020) (RNA-seq) | BI: 3 | C: 5
  - Significantly downregulated at 32hr across strains (FC -2.1, p=3.9e-10) with inter-strain antisense differences.
- IDC in constant temperature and darkness (2020) (Subudhi et al. 2020) (RNA-seq) | BI: 4 | C: DE not available
  - Peak sense-strand expression at 40hr (FC 17.8) with antisense cycling, suggesting intrinsic transcriptional rhythmicity.
- Pfal3D7 real-time transcription and decay () | BI: 4 | C: DE not available
  - Stable nascent transcription with mid-cycle suppression in stable mRNA fraction, suggesting post-transcriptional regulation contributes to trophozoite-stage mRNA reduction.
- Transcriptome of the asexual life stages (Tang et al. 2020) (RNA-seq) | BI: 3 | C: 5
  - Significantly upregulated in schizonts versus rings (FC 3.0, p=6.2e-5) and significantly downregulated in trophozoites versus sporozoites (p=2.6e-18).
- Strand specific transcriptomes of 4 life cycle stages (Lopez-Barragan et al.) (RNA-seq) | BI: 3 | C: DE not available
  - Strongly upregulated from trophozoite to schizont on both strands (sense FC 8.3, antisense FC 7.9) with secondary gametocyte V enrichment.
- Life cycle expression data (3D7) (Le Roch et al.) (array) | BI: 4 | C: DE not available
  - Peaks at late schizogeny (expression 5.24) with upregulation from early to late schizogeny (FC 1.8, top 18.8%).

### Sporozoite and Mosquito Stage Expression

This gene is consistently and strongly downregulated in sporozoites compared to blood stages, with significant downregulation also observed during the oocyst-to-sporozoite transition. Mosquito sporozoites show the strongest suppression relative to asexual blood stages (FC -45.7, p=6.3e-6).

- Mosquito or cultured sporozoites and blood stage transcriptome (NF54) (Hoffmann et al.) (RNA-seq) | BI: 4 | C: 5
  - Strongly downregulated in mosquito sporozoites (FC -45.7, p=6.3e-6) and cultured sporozoites (FC -12.6, p=0.044) compared to asexual blood stages.
- Oocyst and salivary gland sporozoite transcriptome comparison in <i>P. falciparum</i> (Lindner et al.) (RNA-seq) | BI: 4 | C: 5
  - Substantially downregulated in salivary gland sporozoites compared to oocysts (FC -8.2, p=1.2e-7), indicating expression loss during sporozoite maturation.
- Comparison of in vitro versus aseptic mosquito produced sporozoites by RNA-seq (Eappen et al. 2022) (RNA-seq) | BI: 4 | C: DE not available
  - Strongly downregulated in mosquito-produced versus in vitro sporozoites on the sense strand (FC -20.9, top 11.1%) with opposing antisense changes.
- Asexual blood stages, salivary gland sporozoite and midgut oocyst transcriptomes (Gomez-Diaz) (RNA-seq) | BI: 5 | C: DE not available (antisense only)
  - Modest antisense upregulation in oocysts and sporozoites versus asexual blood stages (top 1.6–4.9% upregulated).

### Sexual Stage and Gametocyte Expression

The gene is upregulated in sexually committed schizonts (FC 1.8, top 8.9%) and shows progressive downregulation following gametocyte induction, with relatively stable expression across gametocyte stages I–V and peak absolute expression at gametocyte stage V (22.17 TPM).

- Sexually vs asexually committed schizont transcriptional profiles (Pelle et al.) (array) | BI: 5 | C: DE not available
  - Upregulated in sexually committed versus asexually committed schizonts (FC 1.8, top 8.9%).
- Gametocyte time course from commitment to maturity (van Biljon et al.) (array) | BI: 4 | C: DE not available
  - Progressively downregulated following gametocyte induction, with peak suppression at day 6 (FC -2.2, top 17.6%).
- Gametocyte stages I-V transcriptomes (Young et al.) (array) | BI: 2 | C: DE not available
  - Relatively highly expressed across all gametocyte stages (top 20.9%) with stable expression through stages I–V.
- Transcriptomes of 7 sexual and asexual life stages (Lopez-Barragan et al.) (RNA-seq) | BI: 4 | C: DE not available
  - Peaks in gametocyte V (22.17 TPM) with notable upregulation from gametocyte II to V (FC 4.6, top 17.1%).

### Clinical and Field Isolate Expression

In clinical isolates from Gambian children, mild upregulation in uncomplicated versus severe malaria is observed (FC 1.8, p=0.021 for cerebral malaria with hyperlactatemia vs uncomplicated) with a significant sex-based difference (p=0.003).

- Dual transcriptomes of malaria-infected Gambian children (RNA-Seq) | BI: 5 | C: 2
  - Mild but consistent upregulation in uncomplicated malaria versus severe phenotypes with significant sex-based differences.
- NSR-seq Transcript Profiling of malaria-infected pregnant women and children (Vignali et al.) (RNA-seq) | BI: 5 | C: DE not available
  - Upregulated approximately 2-fold in 3D7 reference compared to field isolate pools (FC 1.9–2.1, top 10%).

### Epigenetic and Perturbation Studies

Heat-shock-sensitive mutants show notable antisense upregulation, particularly in ΔDHC (FC 2.1, top 0.5%). The gene is modestly downregulated upon PfBDP1 knockdown (top 8.3%) and shows potential co-regulation with invasion ligands in EBA knockout lines.

- Heat shock response in sensitive mutants (LRR5, DHC) (Zhang et al. 2021) (RNA-seq) | BI: 5 | C: DE not available (not tested)
  - Antisense upregulation in ΔDHC mutant (FC 2.1, top 0.5%) and ΔLRR5 (FC 1.6, top 8.6%).
- Transcriptome of Bromodomain protein conditional knockouts over the IDC (Josling et al. 2015) (array) | BI: 5 | C: DE not available
  - Modestly downregulated upon PfBDP1 knockdown (FC -1.1, top 8.3%).
- Invasion pathway knockouts (Stubbs et al.) (array) | BI: 5 | C: DE not available
  - Moderately downregulated in EBA140 and EBA175 knockout lines (FC -1.3, top 8.8–14.6%).
- Two Sir2 KO lines expression profiling (array) | BI: 3 | C: DE not available
  - Minimal expression changes in sir2a and sir2b knockout lines across erythrocytic stages.
- Three Isogenic Lines w/ CQ Treatment: expression profiles (Jiang et al.) (array) | BI: 4 | C: DE not available
  - Modestly upregulated upon chloroquine treatment in wild-type and CQ-resistant lines (FC 1.1, top 11–14%).

### Cytoadherence and Sequestration

Modest upregulation in ICAM1-binding parasites compared to CD36-binding (FC 1.9) and HBEC-5i-binding (FC 2.2) phenotypes suggests potential association with cytoadherence phenotype variation.

- Transcriptome of sequestration phenotypes (Kamaliddin et al) (RNA-seq) | BI: 4 | C: DE not available
  - Modest upregulation in ICAM1-binding parasites versus CD36-binding (FC 1.9, top 29.9%) and HBEC-5i-binding (FC 2.2, top 22.6%).

### Other

- Gametocyte Transcriptomes (Lasonder et al.) (RNA-seq) | BI: 0 | C: DE not available
  - Minimal differential expression between male and female gametocytes on both strands, indicating no sex-specific expression pattern.
- High resolution intraerythrocytic time course transcriptome by RNA-Seq (Kucharski and Tripathi et al.) (RNA-seq) | BI: 1 | C: DE not available
  - Peaks at 38hr (FC 3.7) and 42hr (FC 3.0) but most fold changes rank in upper 50th percentile, indicating modest relative changes.
- Intraerythrocytic development cycle transcriptome by UTR-Seq (2020) (Chappell et al. 2020) (RNA-seq) | BI: 0 | C: 5
  - Highly expressed gene (top 7.8%) with statistically significant but small absolute fold changes (-1.2 to -1.4) at mid-cycle.
- Polysomal and steady-state asexual stage transcriptomes (Bunnik et al.) (RNA-seq) | BI: 1 | C: 0
  - Divergent polysomal enrichment across stages with no significant overall difference (p=0.37).
- Ring, Oocyst and Sporozoite Transcriptomes (Zanghi et al.) (RNA-seq) | BI: 4 | C: 0
  - Large sense-strand fold change from oocyst to ring (FC -20.9) but not statistically significant (p=0.15).
- Strand specific transcriptome of the intraerythrocytic developmental cycle (Siegel et al.) (RNA-seq) | BI: 0 | C: DE not available
  - Progressive downregulation through the IDC from 10hr to 40hr with middle-ranked changes.
- Transcriptome in severe vs uncomplicated malaria (Tonkin-Hill et al 2018) (RNA-seq) | BI: 0 | C: 0
  - No meaningful difference between severe versus uncomplicated malaria with non-significant p-values.
- Trophozoite and Schizont transcriptomes of PfBDP1HA (Josling et al 2015) (RNA-seq) | BI: 0 | C: 0
  - Modest non-significant downregulation from schizont to trophozoite in PfBDP1HA background (p=0.37–0.64).