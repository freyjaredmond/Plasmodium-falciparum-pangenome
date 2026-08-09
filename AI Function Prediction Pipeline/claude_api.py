import os
import pandas as pd
from dotenv import load_dotenv
import anthropic
import json
import subprocess

# Load environment variables
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
gene_id_df=pd.read_csv("unknown_genes.tsv", sep="\t")
gene_list=gene_id_df["gene_id"].to_list()

def create_gene_analysis_prompt(trans_data,additional_data, coexpression_data, localisation_data, mapx_data):
    return (
        f"Your task is to analyse all the data provided for a Plasmodium falciparum gene and predict its function \n "
        f"You are provided with five data sections: two TSVs (transcriptomics, additional data) and three plain-text summaries (coexpression, localisation, binding):\n"
        f"A transcriptomics TSV that contains the results of several RNA seq experiments\n"
        f"The RNA seq TSV provided contains\n"
        f" - The experiments with data type listed in brackets (RNA_seq/array) \n"
        f" - A brief description of the study to aid in the understanding of the comparisons made \n"
        f" - The relevant comparisons made (may be multiple comparisons per experiment)\n"
        f" - The differential expression (p-values and effect size). Note, differential expression is only available for experiments that had multiple samples \n"
        f" - Fold changes, the fold change rank and percentile in respect to all other genes within the experiment. This is available for both RNA-seq and array data \n"
        f"**NOTE**\n"
        f"• RNA-seq may have both antisense and sense mRNA- take care to investigate the antisense data also\n"
        f"• Fold Change: positive = upregulated in comparison vs reference; negative = downregulated\n"
        f"• Fold Change Rank: Genes are ranked separately within upregulated (FC > 0) and downregulated (FC < 0) groups. Within each group, rank 1 = most extreme fold change (highest positive for upregulated; most negative for downregulated)-Ties receive the same rank (min ranking).\n"
        f"• Fold Change Percentiles: For both RNA-seq and microarray data, a gene at Top 5% means only 5% of genes in that experiment are more strongly up/downregulated. Lower % = more extreme change.\n"
        f"• RNA-seq Reference and Comparison expression values are measured in TPM, floor values are available in brackets if provided\n"
        f"• Expression rank/percentiles = the reference expression values were ranked (minimum ranking) where rank 1= highest expression at reference condition. The percentiles are calculated so that a percentile of 20% means that the gene is  among the top 20% most highly expressed genes under the reference condition \n"
        f"When interpreting the Fold Change rank and percentiles, take care to also consider the expression ranking and percentile as a lowly expressed genes may show misleading high rank fold changes \n "
        f"• Microarray Reference and Comparison values are given- Note that for some studies the reference and comparison values are given as log2 whereas for others they are raw values \n"
        f"In experiments with low overall transcriptional variation high percentile scores may reflect low absolute fold changes, ensure you treat these values with caution \n"
        f"• For RNA-seq differential expression analysis p-values are given, the percentile of how significant that p-value relative to all other p-values in that comparison is also given\n"
        f"• For RNA-seq differential expression analysis effect size percentile is given, with effect size being ranked separately within upregulated (effect size > 0) and downregulated (effect size < 0) groups. Within each group, rank 1 = most extreme effect size (highest positive for upregulated; most negative for downregulated)-Ties receive the same rank (min ranking). Effect size percentile a gene at top 5% means only 5% of genes in that experiment received an effect size that large. Lower % = more extreme change.\n"
        f"---TRANSCRIPTOMICS DATA---\n"
        f"{trans_data}\n"
        f" You are also provided with an additional data TSV which contains \n"
        f"- The peptide counts taken from several mass spectrometry experiments\n"
        f"- -The total number of available samples (63)\n"
        f"- -The total number of samples that have >0 peptides for that protein\n"
        f"- -The total number of times a unique peptide is identified summed across all samples\n"
        f"- -The number of unique peptides detected across all samples\n"
        f"- Quantitative proteomics data (direct confidence comparison and fold change)\n"
        f"-- The study, description of the study and the comparisons being tested are given\n"
        f"-- For direct confidence comparison experiments the p-value and fold change is given with percentile rankings (as described in the transcriptomics section) being provided\n"
        f"-- For fold change experiments the fold change is given with percentile rankings (as described in the transcriptomics section) being provided \n"
        f"--Note that for some studies the reference and comparison values are given as log2 whereas for others they are raw values\n"
        f"-Post Translational Modification Data\n"
        f"-- The type and number of PTM sites are given \n"
        f"-Mutagenesis piggyBac insertion mutagenesis\n"
        f"--The mutant fitness score is given for a mutagenesis piggyBac insertion mutagenesis investigation \n"
        f"**NOTE**- Data may not be available for all of these metrics \n"
        f"---ADDITIONAL DATA---\n"
        f"{additional_data}\n"
        f"A coexpression summary that contains the product descriptions and GO terms of WGCNA correlated genes\n"
        f"-- A WGCNA experiment was run and the top 50 genes (TOM similarity) within that gene's module were identified \n"
        f"-- The product description for each of these 50 genes is given individually; the GO terms across all 50 genes are given as a ranked frequency count (term and the number of genes annotated with it), not per-gene \n"
        f"-- WGCNA data will not be available if the gene of interest was assigned to a grey module \n "
        f"** Note**: in preliminary investigations, exact GO term matching between a gene of interest and its top 50 co-expressed genes yielded a median match rate of 20%, with cellular component annotations accounting for the majority of matches.\n"
        f" Therefore treat WGCNA with caution and do not weight the WGCNA results as highly in your functional prediction if the WGCNA coexpressed GO terms show multiple themes \n"
        f" Also weight the cell compartment GO terms more highly than the molecular function and biological process GO terms\n "
        f"---COEXPRESSION DATA---\n"
        f"{coexpression_data}\n"
        f"A localisation summary that contains the subcellular niche and GO terms of genes within that subcellular niche \n"
        f"- Data was taken from a hyperLOPIT investigation which classified 1,646 proteins into 21 subcellular niches \n"
        f"- **NOTE**- localisation data may not be available for this gene \n"
        f"- The assigned subcellular niche is provided \n"
        f"- The GO terms of all genes within that subcellular niche are provided as a ranked frequency count (term and the number of genes in the niche annotated with it), not per-gene \n"
        f"- Where possible, the product descriptions of genes that are both in the previously provided WGCNA coexpressed gene list and in the same subcellular niche are provided \n"
        f"---LOCALISATION DATA---\n"
        f"{localisation_data}\n"
        f"A binding summary containing literature supported and MAPX supported protein interaction data \n"
        f"- Gold standard interactions (protein complexes and multimeric proteins) for the gene of interest were manually curated by surveying the P. falciparum proteome and literature\n"
        f"- GO terms are given for all gold standard interactors as a ranked frequency count (term and the number of interactors annotated with it), not per-interactor \n"
        f"- Meltome-assisted profiling of protein complexes (MAP-X) was carried out across several IDC time points \n"
        f"- Interactors that surpassed a precision >0.8 (when mapped to the gold standard data) are provided, along with a count of how many times that interaction recurred (e.g. across different conditions); GO terms for all these interactors are also provided as a ranked frequency count \n"
        f" **NOTE**- the gold standard interactors should be weighted higher than the MAPX interactors in your decision making \n"
        f" Interaction data may not be available for the gene of interest \n"
        f"---BINDING DATA---\n"
        f"{mapx_data}\n"
        f"******OUTPUT FORMAT******\n"
        f"Use these five markdown headers, in this order:\n"
        f"## Predicted Functions\n"
        f"- Five potential functions of this gene (short sentence), ranked in order of likelihood. No justification here, that belongs in the Evidence section \n"
        f"## Summary\n"
        f"A short paragraph (max 100 words) giving your high-level conclusion on this gene's function (combining all data types). This is the takeaway only, not the supporting detail \n"
        f"## Evidence\n"
        f"One short paragraph per available data type, detailing what in that data type led you to predict this function; provide the specific data (values, GO terms, interactors etc.) that led you to these conclusions \n"
        f"## Confidence\n"
        f"A short paragraph describing your confidence in your combined summary, discuss any contradictions and concerns across data types \n"
        f"## Experimental Validation\n"
        f"A short paragraph to describe how this function could be experimentally or bioinformatically confirmed \n"
        f"***NOTE***: if any data type is unavailable, skip its paragraph in the Evidence section rather than speculating \n"
        f"**OUTPUT:** Markdown text only. No preamble, no code blocks, no JSON. Please wrap user-facing species names in `<i>` tags and use clear, scientific language accessible to non-native English speakers.\n")


    

#run the overall pipeline
def analyse_gene_expression(gene_id):
    try:
        # Load data
        trans_data= pd.read_csv(f"data_outputs/{gene_id}/transcriptomics.tsv", sep="\t")
        trans_data = trans_data.to_string()
        additional_data= pd.read_csv(f"data_outputs/{gene_id}/combined_prompt_data.tsv", sep="\t")
        additional_data= additional_data.to_string()
        with open(f"data_outputs/{gene_id}/wgcna_data.txt", encoding="utf-8") as f:
            coexpression_data=f.read()
        with open(f"data_outputs/{gene_id}/location_data.txt", encoding="utf-8") as f:
            location_data=f.read()
        with open(f"data_outputs/{gene_id}/mapx_data.txt", encoding="utf-8") as f:
            mapx_data=f.read()
      
        # Analysis of all experiments
        print(f"Analysing {gene_id}...")
        prompt1 = create_gene_analysis_prompt(trans_data, additional_data, coexpression_data, location_data, mapx_data)
        
        message1 = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=10000,  
            messages=[{"role": "user", "content": prompt1}]
        )
        
        print("Individual experiment analysis completed")
        meta_markdown = message1.content[0].text.strip()
        os.makedirs(f"data_outputs/{gene_id}/Prompt_outputs", exist_ok=True)
        md_path = f"data_outputs/{gene_id}/Prompt_outputs/expression_pipeline_{gene_id}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(meta_markdown)
        return {
            "gene_id": gene_id,
            "meta_analysis": meta_markdown,
            "token_usage": {
                "stage1_input": message1.usage.input_tokens, #see how much you used
                "stage1_output": message1.usage.output_tokens,
                "total": message1.usage.input_tokens + message1.usage.output_tokens  #total amount you used
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
            json_path = f"data_outputs/{gene}/Prompt_outputs/all_gene_analysis_results_{gene}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"Finished {gene} ({i+1}/{len(gene_list)})")

main()