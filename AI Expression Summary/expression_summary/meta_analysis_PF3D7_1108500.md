**Oocyst-Enriched, Trophozoite-to-Schizont Peaking Gene with Rapid mRNA Turnover and Female Gametocyte Antisense Transcription**

This gene exhibits peak expression during the mid-to-late intraerythrocytic developmental cycle (IDC) and in midgut oocysts, with strong silencing in sporozoites. During the asexual blood stage, expression rises dramatically from ring to trophozoite-schizont stages (FC 21.8 at 34 hpi vs 4 hpi, top 7.8% upregulated), confirmed across multiple datasets and strains. In mosquito stages, expression peaks in oocysts and is profoundly downregulated in salivary gland sporozoites (FC −24.6, top 4.5%, p=6.5e-24). Key findings:

- **Oocyst-enriched**: strongly upregulated in oocysts versus blood stages (FC 3.6, top 0.9%, p=1.2e-6) with dramatic silencing upon sporozoite maturation
- **Trophozoite-schizont peak**: replicated across IDC datasets with high statistical support (FC 7.7, p=2.9e-17 in trophozoites vs rings)
- **Female-biased antisense transcription**: antisense strand enriched in female versus male gametocytes (FC 6.9, top 3.7%)
- **Rapid mRNA turnover**: transcripts driven entirely by active transcription with no detectable stable mRNA pool
- **Epigenetic sensitivity**: upregulated in SIR2 knockout (FC 2.0, top 1.2%) and mildly in Sir2b knockout

These patterns suggest a role in replicative or metabolic processes active during schizogony and oocyst development, potentially under epigenetic regulation.

---

## Key Experiments

### Intraerythrocytic Development Cycle Expression

This gene consistently peaks during the trophozoite-to-schizont transition across multiple strains and experimental platforms, with fold changes ranging from 5.7 to 52.3 over ring-stage baselines. High-confidence replicated datasets confirm upregulation in trophozoites (FC 7.7, p=2.9e-17) and schizonts (FC 6.9, p=6.2e-13) versus rings.

- Blood stage transcriptome (3D7) (Otto et al.) (RNA-seq) | BI: 5 | C: N/A
  - Expression peaks at 32 hpi during the trophozoite-to-schizont transition (FC 4.2 vs 0hr, top 10.7% upregulated) and is strongly downregulated at early time points (FC -2.7 at 8hr, top 5.5% downregulated), consistent with a mid-to-late IDC expression profile.
- High resolution intraerythrocytic time course transcriptome by RNA-Seq (Kucharski and Tripathi et al.) (RNA-seq) | BI: 5 | C: N/A
  - Expression rises dramatically from early ring stage, peaking at 34 hpi (FC 21.8 vs 4hr, top 7.8% upregulated) and remaining elevated through schizogony (FC 16.1 at 30hr, FC 14.2 at 38hr), before declining toward reinvasion at 52hr.
- IDC in constant temperature and darkness (2020) (Subudhi et al. 2020) (RNA-seq) | BI: 5 | C: N/A
  - Sense-strand expression peaks at 32 hpi (FC 52.3 vs 0hr, top 29.1% upregulated) with early downregulation at 8hr (FC -7.4, top 10.5% downregulated), revealing a robust mid-cycle expression peak independent of external cues.
- Intraerythrocytic development cycle transcriptome (2018) (Toenhake et al.) (RNA-seq) | BI: 5 | C: N/A
  - Antisense expression peaks at T35–T40 (FC 6.1–8.0, top 5.4–12.7% upregulated), while sense strand shows inverse dynamics during early-to-mid IDC before recovering at T35–T40.
- Intraerythrocytic development cycle transcriptome (2019) (Wichers et al. 2019) (RNA-seq) | BI: 5 | C: 4
  - Strongly upregulated from late ring to mid-trophozoite (FC 10.3, top 5.6% upregulated, p=3.0e-5) with peak expression at early schizont stage, followed by significant downregulation from late schizont to merozoite (FC -2.5, top 8.8%, p=0.015).
- Intraerythrocytic development cycle transcriptome by DAFT-Seq (3D7, HB3, IT, 2020) (Chappell et al. 2020) (RNA-seq) | BI: 5 | C: 5
  - Antisense transcription peaks at 40hr (FC 3.3, top 0.9% upregulated, p=8.9e-17) with exceptionally strong statistical support across three strains, confirming a conserved mid-to-late IDC expression peak.
- Intraerythrocytic development cycle transcriptome by UTR-Seq (2020) (Chappell et al. 2020) (RNA-seq) | BI: 4 | C: 4
  - UTR-Seq reveals modest upregulation at 32hr (FC 2.8, top 13.8% upregulated, p=4.6e-5).
- Erythrocytic expression time series (3D7, DD2, HB3) (Bozdech et al. and Llinas et al.) (array) | BI: 5 | C: N/A
  - Across all three strains, expression is largely constitutive and low by microarray, with HB3 showing a modest late-stage increase at 31–39 hpi (FC 1.6, top 38.1%).
- Strand specific transcriptome of the intraerythrocytic developmental cycle (Siegel et al.) (RNA-seq) | BI: 4 | C: N/A
  - Expression increases progressively from 10hr through 40 hpi (FC 5.7, top 17.0% upregulated), confirming a trophozoite-to-schizont stage peak.
- Life cycle expression data (3D7) (Le Roch et al.) (array) | BI: 4 | C: N/A
  - Expression increases through trophozoite to early schizogeny (FC 1.5, top 18.2% upregulated) and declines through merozoite stage, confirming a mid-IDC peak.
- Transcriptome of the asexual life stages (Tang et al. 2020) (RNA-seq) | BI: 5 | C: 5
  - Strongly upregulated in trophozoites (FC 7.7, top 19.3%, p=2.9e-17) and schizonts (FC 6.9, top 13.3%, p=6.2e-13) versus rings, with antisense transcription also peaking at schizont stage.
- Trophozoite and Schizont transcriptomes of PfBDP1HA (Josling et al 2015) (RNA-seq) | BI: 3 | C: 4
  - Significantly downregulated in trophozoites compared to schizonts on both antisense (FC -4.1, p=1.1e-5) and sense strands (FC -4.8, p=1.9e-5), confirming higher expression at the schizont stage.

### Mosquito Stage and Sporozoite Expression

Expression peaks in midgut oocysts and is profoundly silenced during sporozoite maturation, with FC −24.6 (p=6.5e-24) in salivary gland sporozoites versus oocysts. Mosquito-derived sporozoites show dramatically lower expression than blood stages (FC −70.4, p=1.3e-6).

- Asexual blood stages, salivary gland sporozoite and midgut oocyst transcriptomes (Gomez-Diaz) (RNA-seq) | BI: 5 | C: 5
  - Strongly upregulated in midgut oocysts versus asexual blood stages (FC 3.6, top 0.9% upregulated, p=1.2e-6) and markedly downregulated in salivary gland sporozoites versus oocysts (FC -4.6, top 15.1%, p=6.9e-14).
- Oocyst and salivary gland sporozoite transcriptome comparison in <i>P. falciparum</i> (Lindner et al.) (RNA-seq) | BI: 5 | C: 5
  - Profoundly downregulated in salivary gland sporozoites compared to oocysts (FC -24.6, top 4.5% downregulated, p=6.5e-24).
- Ring, Oocyst and Sporozoite Transcriptomes (Zanghi et al.) (RNA-seq) | BI: 5 | C: 5
  - Strongly downregulated in sporozoites versus oocysts (FC -4.7, top 12.0%, p=7.4e-8) and significantly downregulated on antisense strand compared to rings (FC -49.0, top 2.3%).
- Mosquito or cultured sporozoites and blood stage transcriptome (NF54) (Hoffmann et al.) (RNA-seq) | BI: 4 | C: 5
  - Dramatically downregulated in mosquito sporozoites versus asexual blood stages (FC -70.4, top 15.3%, p=1.3e-6), indicating strong silencing specifically in mature mosquito-derived sporozoites.
- Comparison of in vitro versus aseptic mosquito produced sporozoites by RNA-seq (Eappen et al. 2022) (RNA-seq) | BI: 4 | C: N/A
  - Modest upregulation in mosquito-produced sporozoites compared to in vitro sporozoites on sense strand (FC 5.0, top 17.5%), though very low baseline expression limits reliability.

### Sexual Stage and Gametocyte Expression

This gene is highly expressed throughout gametocyte development with female-enriched antisense transcription (FC 6.9, top 3.7% in females vs males). Expression is sustained from early to late gametocyte stages.

- Gametocyte Transcriptomes (Lasonder et al.) (RNA-seq) | BI: 5 | C: N/A
  - On the antisense strand, markedly upregulated in females versus males (FC 6.9, top 3.7% upregulated), while sense-strand expression is high in both sexes with minimal differential expression.
- Gametocyte stages I-V transcriptomes (Young et al.) (array) | BI: 5 | C: N/A
  - Highly expressed throughout gametocyte development (reference expression rank top 8.8%) with consistent upregulation from day 1 across all stages.
- Gametocyte time course from commitment to maturity (van Biljon et al.) (array) | BI: 3 | C: N/A
  - Moderate downregulation during mid-gametocyte maturation peaking at day 10 post-induction (FC -2.0, top 28.2% downregulated), suggesting transient repression during stage III–IV development.
- Transcriptomes of 7 sexual and asexual life stages (Lopez-Barragan et al.) (RNA-seq) | BI: 5 | C: N/A
  - Expression increases dramatically from early to late trophozoite (FC 52.8, top 2.7% upregulated), with sustained expression through schizont and gametocyte stages.
- Sexually vs asexually committed schizont transcriptional profiles (Pelle et al.) (array) | BI: 2 | C: N/A
  - Modest upregulation in sexually committed schizonts versus asexually committed schizonts (FC 1.3, top 32.2%).
- Strand specific transcriptomes of 4 life cycle stages (Lopez-Barragan et al.) (RNA-seq) | BI: 3 | C: N/A
  - Highly expressed in trophozoites (189.5 TPM, top 0.9% expression rank) with sustained expression in gametocyte stages and abundant antisense transcription across all stages.

### mRNA Turnover and Translational Regulation

The transcript pool is driven entirely by active transcription during trophozoite-schizont stages with rapid decay and no detectable stable mRNA, while ring-stage polysomal enrichment suggests post-transcriptional regulation.

- Pfal3D7 real-time transcription and decay () | BI: 4 | C: N/A
  - Labelled mRNA peaks at 28–32 hpi (FC 2.8–2.9, top 14–17%) while unlabelled mRNA remains undetectable throughout, indicating rapid mRNA turnover.
- Polysomal and steady-state asexual stage transcriptomes (Bunnik et al.) (RNA-seq) | BI: 3 | C: N/A
  - At ring stage, polysomal mRNA is dramatically enriched over steady-state mRNA (FC 19.2, top 20.4%), suggesting strong translational engagement despite low steady-state abundance.

### Epigenetic Regulation and Knockout Studies

Expression is upregulated in SIR2 knockout parasites (FC 2.0, top 1.2%) and mildly in Sir2b knockout (top 2.0%), suggesting this gene may be subject to Sir2-mediated epigenetic repression. Invasion pathway perturbations also alter expression.

- Invasion pathway knockouts (Stubbs et al.) (array) | BI: 5 | C: N/A
  - Strongly upregulated in SIR2 knockout versus wild-type at 24hr (FC 2.0, top 1.2% upregulated) and shows modest upregulation in PfRh2b KO (FC 1.5, top 7.4%).
- Two Sir2 KO lines expression profiling (array) | BI: 5 | C: N/A
  - Sir2b knockout shows modest upregulation at both schizont (top 4.3%) and trophozoite stages (top 2.0%) compared to wild-type, suggesting mild repression by Sir2b-mediated silencing.

### Clinical and Field Isolate Expression

Expression in clinical field isolates from pregnant women is 3–4 fold higher than laboratory 3D7, though stage composition differences may confound comparisons. No significant association with disease severity was detected.

- Dual transcriptomes of malaria-infected Gambian children (RNA-Seq) | BI: 5 | C: 3
  - No statistically significant differential expression between cerebral malaria, hyperlactatemia, and uncomplicated malaria (all p>0.05), though sex-based comparisons show moderate significance (p=1.6e-4).
- NSR-seq Transcript Profiling of malaria-infected pregnant women and children (Vignali et al.) (RNA-seq) | BI: 3 | C: N/A
  - Field isolates from pregnant women show 3–4 fold higher expression than laboratory 3D7 (FC -3.0 to -3.9 for PLO vs 3D7).

### Cytoadherence and Sequestration

Expression varies with cytoadherence phenotype, showing downregulation in CD36-binding versus brain endothelial cell-binding parasites (FC -3.0 to -3.4, top 14–23%).

- Transcriptome of sequestration phenotypes (Kamaliddin et al) (RNA-seq) | BI: 5 | C: N/A
  - Upregulated in ICAM1-binding parasites on antisense strand (FC 1.4, top 9.0%) and consistently downregulated in CD36-binding versus brain endothelial cell-binding phenotypes.

### Drug Response

Chloroquine treatment causes modest but consistent downregulation across isogenic PfCRT lines.

- Three Isogenic Lines w/ CQ Treatment: expression profiles (Jiang et al.) (array) | BI: 4 | C: N/A
  - Chloroquine treatment causes modest downregulation across all three isogenic PfCRT lines (FC -1.1, top 10–26% downregulated).

### Other

- Heat shock response in sensitive mutants (LRR5, DHC) (Zhang et al. 2021) (RNA-seq) | BI: 4 | C: 0
  - No statistically significant expression changes in either ΔDHC or ΔLRR5 heat-shock-sensitive mutants compared to wild-type NF54 (all p>0.05).
- Transcriptome of Bromodomain protein conditional knockouts over the IDC (Josling et al. 2015) (array) | BI: 0 | C: N/A
  - PfBDP1 conditional knockdown causes negligible change in this gene's expression (FC -1.0, top 53.4%), indicating it is not a direct transcriptional target of PfBDP1.
- Transcriptome in severe vs uncomplicated malaria (Tonkin-Hill et al 2018) (RNA-seq) | BI: 4 | C: 0
  - Non-significant trend toward upregulation in severe versus uncomplicated malaria on the sense strand (FC 2.9, p=0.30), with no significant difference on antisense strand (p=0.49).