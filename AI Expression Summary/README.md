## Statistical AI Transcriptomics Expression Summary
The PlasmoDB AI expression transcriptomics expression summary was modified to incorporate:
- Different expression statistics
- Fold change directional expression percentiles
- Explicit biological importance and confidence scores

RNA-seq and microarray data was taken from PlasmoDB was taken for all major comparisons. 
Transcriptomics data was collated into a TSV for each gene of interest using the following
script [GET_transcriptomics](get_expression_data.py). This script also assigns biological
importance and confidence scores.
The output is here [transcriptomics_data](transcriptomics_data)

Claude was then asked to summarise the transcriptomics data using the following prompt
[Claude comparison](claude_get_report.py)
Here, the AI is first asked to summarise each individual experiment with a focus on statistical
and contextual support. Then the AI is asked to summarise all individual per summary experiments
to identify the most important findings.
The output is here [expression_summary](expression_summary)

# Comparing prompts
The original beta PlasmoDB expression summary and the new statistical based summary were compared using
[comparison_prompt.py](comparison_prompt.py)
The output is here [comparison_output](comparison_output)
