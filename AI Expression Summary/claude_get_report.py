### The script used to generate the AI transcriptomics expression summary from transcriptomics data
### The pipeline consists of two prompts- one to summarise each individual experiment and one to synthesise all per experiment summaries
### The output is given in markdown
import os
import pandas as pd
from dotenv import load_dotenv
import anthropic
import json


# Load environment variables
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
gene_list = ["PF3D7_0420100","PF3D7_1352100","PF3D7_1470700","PF3D7_1313800","PF3D7_1117700","PF3D7_0423700","PF3D7_1108500",
                "PF3D7_1032400","PF3D7_0607300","PF3D7_0710900"]


#create the prompt for the first section
def create_gene_analysis_prompt(tsv_data):
    return (
        f"Your task is to analyse RNA-seq and microaaray data for a single gene for each transcriptomics experiment listed in the provided TSV. \n "
        f"The TSV provided contains:\n"
        f" - The experiments with data type listed in brackets (RNA_seq/array) \n"
        f" - A brief description of the study to aid in the understanding of the comparisons made \n"
        f" - The relevant comparisons made (may be multiple comparisons per experiment)\n"
        f" - The differential expression (p-values and effect size). Note, differential expression is only available for experiments that had multiple samples \n"
        f" - Fold changes, the fold change rank and percentile in respect to all other genes within the experiment. This is available for both RNA-seq and array data \n"
        f"{tsv_data}\n\n"
        f"• RNA-seq may have both antisense and sense mRNA- take care to investigate the antisense data also\n" 
        f"• Fold Change: positive = upregulated in comparison vs reference; negative = downregulated\n" 
        f"• Fold Change Rank: Genes are ranked separately within upregulated (FC > 0) and downregulated (FC < 0) groups. Within each group, rank 1 = most extreme fold change (highest positive for upregulated; most negative for downregulated)-Ties receive the same rank (min ranking).\n"
        f"• Fold Change Percentiles: For both RNA-seq and microarray data, a gene at Top 5% means only 5% of genes in that experiment are more strongly up/downregulated. Lower % = more extreme change.\n"
        f"• RNA-seq Reference and Comparison expression values are measured in TPM, floor values are available in brackets if provided\n"
        f"• Microarray Reference and Comparison values are given- Note that for some studies the reference and comparison values are given as log2 whereas for others they are raw values \n"
        f"• Expression rank/percentiles = the reference expression values were ranked (minimum ranking) where rank 1= highest expression at reference condition. The percentiles are calculated so that a percentile of 20% means that the gene is  among the top 20% most highly expressed genes under the reference condition \n"
        f"When interpreting the Fold Change rank and percentiles, take care to also consider the expression ranking and percentile as a lowly expressed genes may show misleading high rank fold changes \n "
        f"**NOTE**: In experiments with low overall transcriptional variation high percentile scores may reflect low absolute fold changes, ensure you treat these values with caution \n"
        f"• For RNA-seq differential expression analyis p-values are given, the percentile of how significant that p-value relative to all other p-values in that comparison is also given\n"
        f"• For RNA-seq differential expression analysis effect size is given \n" 
        
        f"- Each comparison has a precalculated biological importance scoreas well as a confidence score \n"
        f"- These were determined using the following criteria:\n"

        f"2. **Biological_importance score**: Integer 0-5 scale (0 lowest, 5 highest)\n"
        f"  0= No meaningful change (FC percentile >50%)\n"
        f"  1= Small change (FC percentile <50% and >40%)\n"
        f"  2= Modest Change (FC percentile <40% and >30%)\n"
        f"  3= Substantial change (FC percentile <30% and >20%)\n"
        f"  4= Large change (FC percentile <20% and >10%)\n"
        f"  5= Exceptional change (FC percentile <10%)\n"

        f"3. **Confidence_score**: Integer 0-5 (0 lowest, 5 highest)\n"
        f"  DE Not Available = No differential expression data available\n"
        f"  0= No statistical support: P value >0.05\n"
        f"  1= Low statistical support: P value <0.05 and >=0.01\n"
        f"  2= Adequate statistical support: P value <0.01 and >=0.001 b\n"
        f"  3= Moderate statistical support: P value <0.001 and >=0.0001\n"
        f"  4=Strong statistical support: P value <0.0001\n"
        f"  5= Exceptional statistical support: P value <0.00001\n"

        f"**FOR EACH EXPERIMENT:**\n"
        f"**CRITICAL**- write one sentence per study- all comparisons should be contained into one sentence\n"
        f"1. **Summary**: One sentence (STRICTLY maximum 50 words) describing the gene's expression change. Write in clear narrative prose do not list statistics in isolation. Integrate p-values, fold changes and percentiles into sentences to justify your findings e.g This gene is strongly downregulated in mosquito sporozoites compared to blood stages (FC -48.8, top 22% of downregulated genes, p=1.4e-8). DO NOT make statements that aren't supported by the data. The summary should be accessible to a biologist browsing the database, not just a statistician.\n"
        f"    Structure: Lead with the biological finding in plain language, then support with one set of key statistics in brackets. Synthesise across all comparisons into one coherent biological statement — do not list each comparison separately- one sentece should contain all. \n"
        f"   - Wrap species names in <i> tags\n" 
        f"   - Report antisense findings if notable expression changes are found \n"
        f"   - Report the precalcualted biological importance scores and confidence scores in the following format for the **HIGHEST** score achieved by any comparison in that study using the following format:\n"
        f"   - Biological Importance 5 | Confidence 3\n"
        f"4.**optional notes**: Only report if there are peculiarities or caveats that may aid interpretation and further analysis (max 20 words)\n"
        f"5. **keywords**: 3-5 experiment-type keywords\n"
        f"6. **dataset_id**: Use the study name as identifier\n"
        
        f"**OUTPUT FORMAT:** Valid JSON with each experiment as a separate object.\n")
        
#create the prompt for the second section
def create_meta_analysis_prompt(json_data):
    return (
        f"**META-ANALYSIS OF GENE EXPRESSION**\n"
        f"Below are AI-generated summaries of one gene's expression across multiple transcriptomics experiments, your task is to generate a transcriptomics expression summary for biologists using the PlasmoDB data base:\n"
        f"{json_data}\n"
        
        f"**GENERATE:**\n"
        f"1. **headline**: Short, specific title reflecting this gene's key expression pattern-avoid generic phrases like 'comprehensive insights' or 'gene expression, make bold text\n"    
        f"2. **summary**: A summary describing the main expression patterns-**CRITICAL** DO NOT discuss comparisons and studies that did not have significant or important findings \n"
        f"   - Include available statistics where important, write in clear narrative prose do not list statistics in isolation. Integrate p-values, fold changes and percentiles into sentences to justify your findings e.g This gene is strongly downregulated in mosquito sporozoites compared to blood stages (FC -48.8, top 22% of downregulated genes, p=1.4e-8). DO NOT make statements that aren't supported by the data. The summary should be accessible to a biologist browsing the database, not just a statistician.\n"
        f"   - Wrap species names in <i> tags\n"
        f"   - Key findings should be listed in bullet points \n"
        f"   - The summary including the bullet points should be 100-150 words \n"
        f"   - Include a sentence speculating on potential function only if strongly supported by data at the end\n"
        f"3. **key experiments**: Group qualifying experiments by broad biological theme.\n"
        f"   **INSTRUCTION** You must include studies in the key experiments if they pass these inclusion rules (use this table exactly):\n"
        f"   | Biological importance | Confidence | Include? |\n"
        f"   |---|---|---|\n"
        f"   | >=2 | N/A | YES — no test available is not the same as not significant |\n"
        f"   | >=2 | >=1 | YES |\n"
        f"   | >=2 | 0 | NO — tested but not significant |\n"
        f"   | <2 | >=3 | YES |\n"
        f"   | <2 | <3 or N/A | NO |\n"
        f"   DO NOT include studies not meeting these criteria.\n"
        f"   Each topic should be a broad biological theme i.e 'Sexual Stage and Gametocyte Expression','Clincal and Field Isolate Expression\n"
        f"   - **topic headline**: Summarise key experimental results within this topic that are best supported by the data\n"
        f"   - **topic summary**: **CRITICAL**- Include one sentence describing the experimental findings and relevant statistics\n"
        f"   - **experiments**: List of dataset_ids belonging to this topic as bulletpoints and put and their corresponding biological importance and confidence scores (with letters) seperated by |. \n"
        f"   - for each experiment include the expression summary that is in the JSON you were provided with \n"
        f"   - **other (REQUIRED)**: You MUST include a final topic called 'Other' containing ALL experiments that did NOT meet the criteria (Biological_importance_score < 2 OR Confidence_score == 0).For each, include: dataset_id, biological importance score, confidence score, and experiment summary \n"
        f"   - INSTRUCTION **BEFORE OUTPUTTING**: Check each experiment against the inclusion table. Move studies to key experiments if incorrectly placed in other or move studies to other if incorrectly included\n"
        f"   - **OUTPUT:** Markdown text only. No preamble, no code blocks, no JSON. Please wrap user-facing species names in `<i>` tags and use clear, scientific language accessible to non-native English speakers.\n")
    

#run the overall pipeline
def analyse_gene_expression(gene_id):
    try:
        # Load data
        tsv = pd.read_csv(f"transcriptomics_data/{gene_id}_transcriptomics_data.tsv", sep="\t")
        tsv_data = tsv.to_string()
        
        # Analysis of all experiments
        print(f"Analysing {len(tsv)} experiments...")
        prompt1 = create_gene_analysis_prompt(tsv_data)
        
        message1 = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=10000,  
            messages=[{"role": "user", "content": prompt1}]
        )
        
        individual_analysis = message1.content[0].text
        print("Individual experiment analysis completed")
        
        # Clean JSON response (remove markdown formatting if present)
        if "```json" in individual_analysis:
            individual_analysis = individual_analysis.split("```json")[1].split("```")[0].strip()
        
        # Meta-analysis synthesis
        print("Generating meta-analysis...")
        prompt2 = create_meta_analysis_prompt(individual_analysis)
        
        message2 = client.messages.create(
            model="claude-opus-4-6", 
            max_tokens=10000,
            messages=[{"role": "user", "content": prompt2}]
        )
        meta_markdown = message2.content[0].text.strip()
        md_path = f"expression_summary/meta_analysis_{gene_id}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(meta_markdown)
        print("Finished Meta-analysis...")
            
        return {
            "gene_id": gene_id,
            "individual_analysis": individual_analysis,
            "meta_analysis": meta_markdown,
            "token_usage": {
                "stage1_input": message1.usage.input_tokens, #see how much you used
                "stage1_output": message1.usage.output_tokens,
                "stage2_input": message2.usage.input_tokens,
                "stage2_output": message2.usage.output_tokens,
                "total": message1.usage.input_tokens + message1.usage.output_tokens + 
                        message2.usage.input_tokens + message2.usage.output_tokens #total amount you used
            }
        }
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None
#access to the pipeline for all genes
def main():
    for i, gene in enumerate(gene_list):
        print(f"\nProcessing {gene} ({i+1}/{len(gene_list)})")
        results = analyse_gene_expression(gene_id=gene)
        if results:
            json_path = f"expression_summary/all_gene_analysis_results_{gene}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"Finished {gene} ({i+1}/{len(gene_list)})")

main()
