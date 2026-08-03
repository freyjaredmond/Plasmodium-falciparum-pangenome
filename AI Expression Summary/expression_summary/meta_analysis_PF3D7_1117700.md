**Constitutively high blood-stage gene with dramatic downregulation in sporozoites and progressive decline during gametocyte maturation**

## Summary

This gene is among the most highly expressed during <i>Plasmodium falciparum</i> asexual blood stages, consistently ranking in the top 0.1–3% of expressed genes (~1000–2800 TPM) across multiple datasets. Expression peaks during trophozoite/early schizont stages with modest mid-IDC upregulation (FC ~2–4x at 28–32 hpi).

- **Sporozoite silencing**: Expression drops dramatically in sporozoites compared to blood stages (FC -62 to -82, top 1–17% downregulated, p≤3.1e-4), with further reduction from oocysts to salivary gland sporozoites (FC -5.5 to -7.9, p≤3.1e-6)
- **Gametocyte decline**: Progressive downregulation during gametocyte maturation, strongest at day 8 post-commitment (FC -2.7, top 4.2% downregulated)
- **Translational control**: Polysomal mRNA is substantially reduced at ring stage (FC -6.6), suggesting translational repression
- **Strain differences**: Significantly higher expression in HB3 versus 3D7 (FC 1.5, p=5.3e-23)
- **Antisense dynamics**: Stage-specific antisense transcription, with notable female gametocyte enrichment (FC 6.4, top 4.1%)

These patterns suggest a core role in asexual erythrocytic biology, possibly related to housekeeping metabolism or invasion machinery.

## Key Experiments

### Sporozoite and Mosquito-Stage Expression
This gene is strongly blood-stage-specific, with 60–80-fold downregulation in sporozoites and significant further decline during sporozoite maturation from oocyst to salivary gland.

- Mosquito or cultured sporozoites and blood stage transcriptome (NF54) (Hoffmann et al.) (RNA-seq) | BI: 5 | C: 5
  - This gene is dramatically downregulated in both cultured sporozoites (FC -81.8, top 1.0% downregulated, p=3.1e-4) and mosquito sporozoites (FC -62.6, top 17.3% downregulated, p=1.0e-10) compared to asexual blood stages (~2336 TPM), with minimal difference between sporozoite types (FC -1.3, p=0.40), confirming strong blood-stage-specific expression.
- Asexual blood stages, salivary gland sporozoite and midgut oocyst transcriptomes (Gomez-Diaz) (RNA-seq) | BI: 5 | C: 5
  - This gene is strongly downregulated in salivary gland sporozoites compared to both asexual blood stages (FC -7.0, top 9.4% downregulated, p=4.2e-6) and midgut oocysts (FC -7.9, top 5.0% downregulated, p=1.0e-9), while showing minimal change between blood stages and oocysts.
- Oocyst and salivary gland sporozoite transcriptome comparison in P. falciparum (Lindner et al.) (RNA-seq) | BI: 3 | C: 5
  - This gene is significantly downregulated in salivary gland sporozoites compared to oocysts on both sense (FC -5.5, top 23.0% downregulated, p=3.1e-6) and antisense strands (FC -5.5, top 23.0% downregulated, p=2.2e-3).
- Ring, Oocyst and Sporozoite Transcriptomes (Zanghi et al.) (RNA-seq) | BI: 5 | C: 5
  - This gene is highly significantly upregulated in rings versus oocysts (FC 7.6, top 11.7% upregulated, p=1.8e-20) and shows significant upregulation of sense transcription from oocyst to sporozoite (FC 3.1, top 14.3%, p=7.5e-19) yet dramatic antisense downregulation in sporozoites versus oocysts (FC -37.3, top 3.7% downregulated, p=0.02).
- Comparison of in vitro versus aseptic mosquito produced sporozoites by RNA-seq (Eappen et al. 2022) (RNA-seq) | BI: 4 | C: N/A
  - This gene is upregulated in mosquito-produced sporozoites compared to in vitro sporozoites on the sense strand (FC 7.6, top 11.7% upregulated), though expression is very low in both conditions (~1.9–14.1 TPM).

### Sexual Stage and Gametocyte Expression
Expression progressively declines during gametocyte maturation, with sex-specific antisense patterns suggesting regulatory complexity.

- Gametocyte time course from commitment to maturity (van Biljon et al.) (array) | BI: 5 | C: N/A
  - This gene shows progressive downregulation during gametocyte maturation, with the strongest decrease at day 8 post-induction (FC -2.7, top 4.2% downregulated) and day 13 (FC -1.6, top 12.0% downregulated).
- Gametocyte Transcriptomes (Lasonder et al.) (RNA-seq) | BI: 5 | C: N/A
  - Antisense transcription is notably upregulated in females versus males (FC 6.4, top 4.1% upregulated) from very low baseline (~1 TPM), while sense-strand expression shows only modest female upregulation (FC 1.7, top 56.4% upregulated) from moderate expression (~180 TPM).
- Gametocyte stages I-V transcriptomes (Young et al.) (array) | BI: 4 | C: N/A
  - This gene is highly expressed throughout gametocytogenesis (log2 ~10.4–11.5, top 0.09% expression rank) with modest downregulation in later stages, peaking at day 6 (FC -1.7, top 13.2% downregulated).

### Intraerythrocytic Development Cycle Expression
The gene is constitutively and highly expressed throughout the IDC with modest mid-cycle peaks, strain-specific variation, and evidence of translational regulation.

- Intraerythrocytic development cycle transcriptome by DAFT-Seq (3D7, HB3, IT, 2020) (Chappell et al. 2020) (RNA-seq) | BI: 3 | C: 5
  - This gene shows significantly higher expression in HB3 versus 3D7 (FC 1.5, p=5.3e-23, top 10.5% significant) and HB3 versus IT (FC -2.0, p=1.5e-11, top 13.6% significant), while IDC temporal changes are modest across all strains.
- Erythrocytic expression time series (3D7, DD2, HB3) (Bozdech et al. and Llinas et al.) (array) | BI: 5 | C: N/A
  - Across three strains (3D7, DD2, HB3), this gene shows very low and stable microarray expression throughout the IDC with minimal fold changes (mostly 1.0–1.4x).
- Intraerythrocytic development cycle transcriptome (2018) (Toenhake et al.) (RNA-seq) | BI: 4 | C: N/A
  - Sense-strand expression is stably high (~1139–2671 TPM) across the IDC with modest 2-fold upregulation at later timepoints, while antisense transcription shows consistent downregulation from T05 baseline, suggesting reciprocal sense/antisense regulation.
- Intraerythrocytic development cycle transcriptome (2019) (Wichers et al. 2019) (RNA-seq) | BI: 5 | C: N/A (DE not available)
  - This gene is stably and highly expressed across all IDC stages (~1000–2820 TPM, top 0.4–2.1%) with no significant differential expression between consecutive stages (all p>0.05).
- IDC in constant temperature and darkness (2020) (Subudhi et al. 2020) (RNA-seq) | BI: 5 | C: N/A
  - Sense-strand expression shows modest decline during the IDC (FC -3.1 to -4.1x at 40–48hr), while antisense transcription shows dramatic upregulation from very low baseline, peaking at 40hr (FC 53.2x, top 6.0% upregulated), indicating stage-specific antisense transcriptional activation during late IDC.
- High resolution intraerythrocytic time course transcriptome by RNA-Seq (Kucharski and Tripathi et al.) (RNA-seq) | BI: 2 | C: N/A
  - This gene shows moderate upregulation during mid-IDC peaking at 30hr (FC 3.9x vs 4hr reference) and 28hr (FC 3.5x), consistent with trophozoite/early schizont peak expression from a moderately expressed baseline (~412 TPM, top 3.4%).
- Pfal3D7 real-time transcription and decay () | BI: 4 | C: N/A
  - Both labelled (nascent) and unlabelled (stable) mRNA fractions show this gene is stably expressed throughout the IDC with minimal transcriptional variation, except the unlabelled fraction shows progressive decline in late stages (FC -2.0 at 44–47hpi), suggesting modest mRNA destabilization during late schizogony.

### Translational Regulation
Polysomal profiling reveals stage-specific translational repression, particularly at ring stage.

- Polysomal and steady-state asexual stage transcriptomes (Bunnik et al.) (RNA-seq) | BI: 4 | C: N/A
  - This gene shows notable translational regulation at ring stage, with polysomal mRNA substantially lower than steady-state (FC -6.6, top 13.8% downregulated), while trophozoite polysomal association is modestly higher (FC 1.5), suggesting stage-specific translational repression particularly at ring stage.

### Life Cycle Stage Profiling
Highly expressed across the full life cycle with consistent blood-stage enrichment.

- Life cycle expression data (3D7) (Le Roch et al.) (array) | BI: 4 | C: N/A
  - This gene is highly expressed across all life cycle stages (log2 ~10.4–11.8, top 0.1–0.3% expression rank), with peak expression at early schizogony (log2 11.80) and upregulation from early trophozoite to late trophozoite.
- Transcriptomes of 7 sexual and asexual life stages (Lopez-Barragan et al.) (RNA-seq) | BI: 2 (see note) | C: N/A
  - This gene is moderately expressed across all seven stages (~440–2182 TPM) with peak expression in late trophozoites, showing gradual decline through schizonts into gametocytes and ookinetes, consistent with constitutive blood-stage expression.

### Invasion Pathway and Epigenetic Regulation
Expression is sensitive to invasion ligand knockouts and subtly altered in epigenetic regulator mutants.

- Invasion pathway knockouts (Stubbs et al.) (array) | BI: 5 | C: N/A
  - This gene is notably downregulated in multiple invasion ligand knockouts versus wildtype, particularly in W2mef EBA175 KO (FC -1.9, top 0.5% downregulated), 3D7 EBA140 KO (FC -1.5, top 3.3%), suggesting invasion pathway-dependent expression regulation.
- Two Sir2 KO lines expression profiling (array) | BI: 5 | C: N/A
  - This gene shows subtle but consistently notable changes in Sir2 knockout lines, with sir2b KO schizonts showing the most pronounced upregulation versus wildtype (FC 1.1, top 4.3% upregulated).
- Heat shock response in sensitive mutants (LRR5, DHC) (Zhang et al. 2021) (RNA-seq) | BI: 5 | C: 1
  - This gene is modestly downregulated in the ΔDHC mutant compared to wildtype on both sense (FC -1.3, top 29.4% downregulated, p=0.024) and antisense strands (FC -1.8, top 7.0% downregulated, p=0.024).
- Transcriptome of Bromodomain protein conditional knockouts over the IDC (Josling et al. 2015) (array) | BI: 3 | C: N/A
  - This gene shows modest upregulation when PfBDP1 is present (FC 1.1, top 25.7% upregulated), suggesting it may be among genes positively regulated by the bromodomain protein PfBDP1.

### Clinical and Field Isolate Expression
Moderate to high expression in clinical samples with no disease-severity association.

- NSR-seq Transcript Profiling of malaria-infected pregnant women and children (Vignali et al.) (RNA-seq) | BI: 2 | C: N/A
  - This gene is moderately expressed in field isolate pools (~1648–1832 TPM) and shows downregulation in the 3D7 reference strain compared to both pregnant women (FC -2.5) and children (FC -2.8) pools.

### Sequestration and Cytoadherence
Expression is high and largely invariant across binding phenotypes.

- Transcriptome of sequestration phenotypes (Kamaliddin et al) (RNA-seq) | BI: 4 | C: N/A
  - This gene is highly expressed across all binding phenotypes (sense: 3211–4038 TPM) with minimal variation between ICAM1, HBEC-5i, and CD36-binding parasites, though antisense shows notable upregulation in HBEC-5i versus ICAM1 binding (FC 1.3, top 11.2% upregulated).

### Drug Response
Expression is unresponsive to chloroquine treatment.

- Three Isogenic Lines w/ CQ Treatment: expression profiles (Jiang et al.) (array) | BI: 4 | C: N/A
  - This gene is highly expressed (log2 ~10.5–10.8) and shows minimal response to chloroquine treatment across all three isogenic PfCRT lines.

### Sexual Commitment
Highly expressed in schizonts with minimal difference between sexually and asexually committed populations.

- Sexually vs asexually committed schizont transcriptional profiles (Pelle et al.) (array) | BI: 2 | C: N/A
  - This gene is highly expressed in schizonts (log2 ~11.6–11.8, top 1.1% expression rank) and shows modest downregulation in sexually committed versus asexually committed schizonts (FC -1.2, top 37.8% downregulated).

### Strand-Specific IDC Profiling
Moderate expression across stages with antisense dynamics in trophozoites.

- Strand specific transcriptomes of 4 life cycle stages (Lopez-Barragan et al.) (RNA-seq) | BI: 2 | C: N/A
  - This gene is moderately expressed across all four stages with highest sense expression in trophozoites (~439 TPM), while antisense expression is notably higher in trophozoites (5128 TPM) with substantial downregulation into schizonts (FC -3.0).

### Other

- Blood stage transcriptome (3D7) (Otto et al.) (RNA-seq) | BI: 0 | C: N/A
  - This gene is moderately and stably expressed across the 48-hour intraerythrocytic cycle in 3D7 (reference ~670 TPM, top 2.8%), with only minor fluctuations peaking at 24–32 hpi (FC ~1.5–1.6x up) and no timepoint showing substantial differential expression.
- Dual transcriptomes of malaria-infected Gambian children (RNA-Seq) | BI: 3 | C: 0
  - This gene shows no significant differential expression across any comparison of cerebral malaria, hyperlactatemia, uncomplicated malaria, or sex in Gambian children (all p>0.05).
- Intraerythrocytic development cycle transcriptome by UTR-Seq (2020) (Chappell et al. 2020) (RNA-seq) | BI: 1 | C: 5
  - This gene shows consistent modest upregulation during mid-IDC peaking at 32hr (FC 1.8, top 46.4% upregulated, p=2.1e-18) with highly significant p-values at multiple timepoints, though absolute fold changes remain small (1.2–1.8x).
- Strand specific transcriptome of the intraerythrocytic developmental cycle (Siegel et al.) (RNA-seq) | BI: 0 | C: N/A
  - This gene is stably expressed across the IDC (945–1488 TPM) with slight upregulation at 20hr (FC 1.4) and minimal variation at other timepoints, indicating constitutive blood-stage expression.
- Transcriptome in severe vs uncomplicated malaria (Tonkin-Hill et al 2018) (RNA-seq) | BI: 1 | C: 1
  - This gene shows no significant differential expression between severe and uncomplicated malaria on either sense (FC 1.1, p=0.017) or antisense strands (FC 1.2, p=0.56).
- Transcriptome of the asexual life stages (Tang et al. 2020) (RNA-seq) | BI: 0 | C: 2
  - This gene is stably expressed across ring, trophozoite, and schizont stages (~1017–1764 TPM) with no significant changes between stages.
- Trophozoite and Schizont transcriptomes of PfBDP1HA (Josling et al 2015) (RNA-seq) | BI: 0 | C: 0
  - This gene shows no significant differential expression between trophozoite and schizont stages in PfBDP1HA parasites on either sense (FC -1.1, p=0.93) or antisense strands (FC -1.1, p=0.72).
- Transcriptomes of 7 sexual and asexual life stages (Lopez-Barragan et al.) (RNA-seq) | BI: 0 | C: N/A
  - This gene is moderately expressed across all seven stages (~440–2182 TPM) with peak expression in late trophozoites, consistent with constitutive blood-stage expression.