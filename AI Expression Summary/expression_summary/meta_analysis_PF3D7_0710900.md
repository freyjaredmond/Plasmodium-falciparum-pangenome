**Trophozoite-Peaking Blood-Stage Gene with Dramatic Silencing in Sporozoites and Enrichment in Female Gametocytes**

This gene is predominantly expressed during the trophozoite stage of the <i>Plasmodium falciparum</i> intraerythrocytic developmental cycle (IDC), with near-complete silencing in sporozoites and notable sexual-stage dimorphism.

- **Blood-stage peak at trophozoite**: Expression consistently peaks at 20–32 hpi across multiple IDC datasets, with robust upregulation at 24 hr (FC 2.7, top 14% upregulated, p=2.3e-15) confirmed by UTR-Seq, then declining through schizogony.
- **Sporozoite silencing**: Dramatically downregulated in mosquito sporozoites versus blood stages (FC -136.9, top 7.2% downregulated, p=5.9e-8), with near-floor expression in salivary gland sporozoites.
- **Strain variation**: Significantly higher expression in HB3 and IT strains versus 3D7 (FC 1.9, p=2.9e-12).
- **Female gametocyte enrichment**: Sense transcripts upregulated ~6.9-fold in female versus male gametocytes; late gametocyte expression increases markedly (FC 6.4, top 10% upregulated).
- **Clinical association**: Downregulated in cerebral malaria with hyperlactatemia versus cerebral malaria alone (FC -2.2, top 5.7% downregulated, p=0.0075).

These patterns suggest a role in active parasite metabolism or erythrocyte remodelling during trophozoite growth, with potential involvement in female gametocyte biology.

---

### Key Experiments

#### Intraerythrocytic Development Cycle Expression

Multiple IDC time-course studies consistently show trophozoite-stage peak expression around 20–32 hpi, with decline during schizogony and significant strain-dependent expression differences.

- **Intraerythrocytic development cycle transcriptome by UTR-Seq (2020) (Chappell et al. 2020) (RNA-seq)** | BI: 4 | C: 5
  - This gene is significantly upregulated during mid-IDC stages, peaking at 24hr (FC 2.7, top 14% upregulated, p=2.3e-15) and remaining elevated at 32hr (FC 2.5, top 21%, p=3.8e-11), with significant downregulation from 24hr to 48hr (FC -2.4, top 20% downregulated, p=1.5e-9), demonstrating robust trophozoite-stage peak expression with high statistical confidence.
- **Intraerythrocytic development cycle transcriptome by DAFT-Seq (3D7, HB3, IT, 2020) (Chappell et al. 2020) (RNA-seq)** | BI: 4 | C: 5
  - This gene is significantly more highly expressed in HB3 (109 TPM) and IT (83 TPM) strains compared to 3D7 (58 TPM; 3D7 vs HB3 FC 1.9, p=2.9e-12; 3D7 vs IT FC 1.4, p=1.3e-5), with IDC time-course showing upregulation at 8hr (FC 2.1, top 17%, p=0.001) and decline by 48hr (FC -1.3), and antisense showing consistent patterns.
- **Intraerythrocytic development cycle transcriptome (2019) (Wichers et al. 2019) (RNA-seq)** | BI: 4 | C: 3
  - Expression remains relatively stable across IDC stages with high baseline expression (~100–157 TPM) and modest fold changes; most notable change is downregulation from schizont to late schizont (FC -1.6, top 17% downregulated).
- **Intraerythrocytic development cycle transcriptome (2018) (Toenhake et al.) (RNA-seq)** | BI: 4 | C: N/A
  - This gene shows progressive upregulation from early ring (T05) peaking at T30–T35 (FC 5.7–5.9, top 27–30% upregulated) in sense and antisense (FC 3.4 at T30, top 15% upregulated), consistent with peak expression during trophozoite-to-schizont transition.
- **High resolution intraerythrocytic time course transcriptome by RNA-Seq (Kucharski and Tripathi et al.) (RNA-seq)** | BI: 4 | C: N/A
  - This gene peaks during mid-IDC stages around 12–30 hpi (FC 2.4–2.9 vs 4hr, top 16–62% upregulated) with highest early induction at 8hr (FC 1.7, top 16%) and 12hr (FC 2.4, top 19%), then declines through late schizogony.
- **Blood stage transcriptome (3D7) (Otto et al.) (RNA-seq)** | BI: 2 | C: N/A
  - During the 3D7 intraerythrocytic cycle, this gene peaks modestly at 24–32 hpi (FC ~2.1 vs 0hr, top 41–46% upregulated) before returning to baseline by 40–48 hpi, indicating mid-trophozoite/early-schizont expression.
- **Erythrocytic expression time series (3D7, DD2, HB3) (Bozdech et al. and Llinas et al.) (array)** | BI: 5 | C: N/A
  - Across 3D7, DD2, and HB3 strains, this gene maintains low and relatively stable expression throughout the IDC with minimal fold changes (mostly FC ≤1.2), though in HB3 a modest decline is seen in late stages.
- **IDC in constant temperature and darkness (2020) (Subudhi et al. 2020) (RNA-seq)** | BI: 2 | C: N/A
  - Under constant temperature and darkness, this gene peaks at 8hr (FC 2.3) and remains elevated through 24–32hr before declining by 40–48hr, with the overall pattern mirroring normal IDC cycling suggesting intrinsic transcriptional regulation.
- **Transcriptome of the asexual life stages (Tang et al. 2020) (RNA-seq)** | BI: 3 | C: 3
  - This gene peaks at trophozoite stage (120 TPM) with upregulation versus ring (FC 2.2) and schizont (FC 3.3, top 28%), while schizont-to-ring shows modest downregulation (FC -1.5, p=0.008).

#### Sporozoite and Mosquito-Stage Expression

This gene is near-silenced in sporozoites, with dramatic downregulation relative to blood stages and oocysts, consistent with blood-stage-restricted function.

- **Mosquito or cultured sporozoites and blood stage transcriptome (NF54) (Hoffmann et al.) (RNA-seq)** | BI: 5 | C: 5
  - This gene is dramatically downregulated in mosquito sporozoites compared to asexual blood stages (FC -136.9, top 7.2% downregulated, p=5.9e-8) and shows substantial upregulation from cultured to mosquito sporozoites (FC 22.8, top 17% upregulated, p=0.002), indicating strong blood-stage-specific expression with near-complete silencing in salivary gland sporozoites.
- **Ring, Oocyst and Sporozoite Transcriptomes (Zanghi et al.) (RNA-seq)** | BI: 5 | C: 5
  - This gene is highly significantly downregulated from oocyst to sporozoite in sense transcripts (p=3.2e-11, effect size -5.3) and from ring to sporozoite (p=1.1e-6, effect size -5.0), with oocyst-to-ring showing strong downregulation (FC -29.3, top 8.4% downregulated), indicating predominant oocyst-stage expression and near-silencing in sporozoites.
- **Asexual blood stages, salivary gland sporozoite and midgut oocyst transcriptomes (Gomez-Diaz) (RNA-seq)** | BI: 5 | C: 4
  - This gene shows modest downregulation from midgut oocyst to salivary gland sporozoite stages (FC -1.0 sense, p=9.8e-5, top 21% downregulated), with antisense transcripts notably upregulated in oocysts versus blood stages (top 1.6% upregulated).
- **Comparison of in vitro versus aseptic mosquito produced sporozoites by RNA-seq (Eappen et al. 2022) (RNA-seq)** | BI: 5 | C: N/A
  - This gene is dramatically downregulated in mosquito-produced sporozoites compared to in vitro sporozoites in both antisense (FC -50.7, top 4.5% downregulated) and sense (FC -29.3, top 8.4% downregulated) transcripts.

#### Sexual Stage and Gametocyte Expression

Expression is enriched in female gametocytes and increases during late gametocytogenesis, with partial repression during sexual commitment.

- **Transcriptomes of 7 sexual and asexual life stages (Lopez-Barragan et al.) (RNA-seq)** | BI: 5 | C: N/A
  - This gene shows strong upregulation from gametocyte II to gametocyte V (FC 6.4, top 10% upregulated) and marked downregulation from late trophozoite to schizont (FC -6.0, top 18% downregulated), with gametocyte V to ookinete also showing decline (FC -3.8).
- **Gametocyte Transcriptomes (Lasonder et al.) (RNA-seq)** | BI: 4 | C: N/A
  - This gene is upregulated in female versus male gametocytes in sense transcripts (FC 6.9, top 19% upregulated) while antisense shows slight downregulation (FC -2.1), suggesting female-enriched sense expression in mature gametocytes.
- **Gametocyte time course from commitment to maturity (van Biljon et al.) (array)** | BI: 4 | C: N/A
  - This gene shows progressive downregulation during late gametocyte maturation, reaching its lowest point at day 8 post-induction (FC -1.8, top 19% downregulated) and day 13 (FC -1.5, top 17% downregulated), with transient early upregulation at day 2.
- **Sexually vs asexually committed schizont transcriptional profiles (Pelle et al.) (array)** | BI: 4 | C: N/A
  - This gene is modestly downregulated in sexually committed schizonts compared to asexually committed schizonts (FC -1.4, top 14% downregulated), suggesting partial repression during sexual commitment.
- **Gametocyte stages I-V transcriptomes (Young et al.) (array)** | BI: 3 | C: N/A
  - This gene maintains relatively stable expression across gametocyte stages I–V with only minor fluctuations (FC range -1.3 to 1.3), showing no dramatic stage-specific regulation during gametocytogenesis.

#### Life Cycle and Multi-Stage Expression

Expression patterns across life stages confirm trophozoite dominance and schizont-stage repression.

- **Life cycle expression data (3D7) (Le Roch et al.) (array)** | BI: 5 | C: N/A
  - This gene is expressed at moderate-to-high levels across erythrocytic stages with notable downregulation from early to late schizogeny (FC -2.0, top 8.3% downregulated) followed by recovery in merozoites (FC 1.4, top 29% upregulated).
- **Strand specific transcriptomes of 4 life cycle stages (Lopez-Barragan et al.) (RNA-seq)** | BI: 3 | C: N/A
  - Antisense transcripts show trophozoite-to-schizont downregulation (FC -4.1, top 22% downregulated) while sense transcripts reveal modest changes; sense expression near floor in schizont and gametocyte stages.

#### Clinical and Field Isolate Expression

Differential expression between malaria severity phenotypes suggests potential association with disease pathology.

- **Dual transcriptomes of malaria-infected Gambian children (RNA-Seq)** | BI: 5 | C: 2
  - This gene shows modest upregulation in uncomplicated versus cerebral malaria (FC 2.0, top 32%, p=0.038) and significant downregulation in cerebral-plus-hyperlactatemia versus cerebral malaria alone (FC -2.2, top 5.7% downregulated, p=0.0075).
- **NSR-seq Transcript Profiling of malaria-infected pregnant women and children (Vignali et al.) (RNA-seq)** | BI: 2 | C: N/A
  - This gene shows modest expression differences between field isolate pools and 3D7, being downregulated in 3D7 compared to both PLO1 (FC -2.5) and PLO2 (FC -3.0), with minimal difference between the two field isolate pools.

#### Epigenetic and Transcriptional Regulation

This gene may be a target of bromodomain and histone deacetylase-mediated regulation.

- **Transcriptome of Bromodomain protein conditional knockouts over the IDC (Josling et al. 2015) (array)** | BI: 5 | C: N/A
  - PfBDP1 knockdown causes notable downregulation of this gene (FC -1.1, top 8.3% downregulated), suggesting it may be among the targets positively regulated by the bromodomain protein PfBDP1 during the IDC.
- **Two Sir2 KO lines expression profiling (array)** | BI: 4 | C: N/A
  - Sir2 knockout lines show subtle but consistently notable changes at schizont stage, with sir2a KO (top 24% downregulated) and sir2b KO (top 15% downregulated) both showing modest repression, while trophozoite and ring stages show slight upregulation.

#### Translational Regulation and mRNA Dynamics

- **Polysomal and steady-state asexual stage transcriptomes (Bunnik et al.) (RNA-seq)** | BI: 3 | C: 1
  - This gene shows higher polysomal than steady-state mRNA levels across all IDC stages, most notably at ring stage (FC 7.5) and schizont stage (FC 2.5, top 28% upregulated), with overall polysomal vs steady-state comparison showing significant translational regulation (p=0.011, effect size -1.74).
- **Pfal3D7 real-time transcription and decay ()** | BI: 3 | C: N/A
  - Both labelled and unlabelled mRNA fractions show modest upregulation peaking around 20–24 hpi (FC 1.7), with transcription and stability profiles closely tracking each other, suggesting this gene's IDC expression pattern is primarily transcriptionally driven.

#### Invasion and Host–Parasite Interaction

- **Invasion pathway knockouts (Stubbs et al.) (array)** | BI: 4 | C: N/A
  - This gene shows modest expression changes across invasion pathway knockouts, with SIR2 KO at 8hr showing the most notable downregulation (FC -1.2, top 12% downregulated) and EBA175 KO at 48hr showing slight upregulation (FC 1.2, top 17% upregulated).
- **Transcriptome of sequestration phenotypes (Kamaliddin et al) (RNA-seq)** | BI: 4 | C: N/A
  - This gene shows minimal sense expression differences between ICAM1-, HBEC-5i-, and CD36-binding parasite lines, though antisense transcripts show more notable upregulation in CD36-binding versus ICAM1- and HBEC-5i-binding lines (top 25–27% upregulated).
- **Three Isogenic Lines w/ CQ Treatment: expression profiles (Jiang et al.) (array)** | BI: 4 | C: N/A
  - Chloroquine treatment produces minimal expression changes in this gene across all three isogenic PfCRT lines, suggesting this gene is not substantially responsive to chloroquine.

#### Other

- **Heat shock response in sensitive mutants (LRR5, DHC) (Zhang et al. 2021) (RNA-seq)** | BI: 4 | C: 0
  - This gene shows modest upregulation in ΔDHC mutants compared to wild-type (FC 1.4, top 31% upregulated) but minimal change in ΔLRR5 mutants (FC -1.0), with none of these changes reaching statistical significance.
- **Transcriptome in severe vs uncomplicated malaria (Tonkin-Hill et al 2018) (RNA-seq)** | BI: 1 | C: 0
  - This gene shows no significant differential expression between severe and uncomplicated malaria in either sense or antisense transcripts from clinical isolates in Papua, Indonesia.
- **Trophozoite and Schizont transcriptomes of PfBDP1HA (Josling et al 2015) (RNA-seq)** | BI: 1 | C: 0
  - This gene shows modest upregulation in trophozoites versus schizonts in PfBDP1HA parasites, with no significant differential expression.
- **Oocyst and salivary gland sporozoite transcriptome comparison in <i>P. falciparum</i> (Lindner et al.) (RNA-seq)** | BI: 1 | C: 1
  - This gene shows no significant change between oocyst and salivary gland sporozoite stages, with expression at very low levels near floor in both conditions.
- **Strand specific transcriptome of the intraerythrocytic developmental cycle (Siegel et al.) (RNA-seq)** | BI: 1 | C: N/A
  - This gene peaks at 20 hpi (FC 1.6) then gradually declines through 30hr and 40hr, showing a broad trophozoite-stage expression profile without dramatic stage-specific changes.