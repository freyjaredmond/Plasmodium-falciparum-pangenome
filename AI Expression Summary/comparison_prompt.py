### The script used to compare the PlasmoDB AI expression summary and the new statistical based summary
### The AI is asked to count the number of observations and insights across each summary, as well as report contradictions
### The AI was also asked to identify which summary performed best in the following metrics: headline, tone, technical detail and overall
### Output is in markdown format
import os
import pandas as pd
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
gene_list = ["PF3D7_0420100","PF3D7_1352100","PF3D7_1470700","PF3D7_1313800","PF3D7_1117700","PF3D7_0423700","PF3D7_1108500",
                "PF3D7_1032400","PF3D7_0607300","PF3D7_0710900"]

def compare_prompts(summary_a, summary_b):
    return (
        f"You are a malaria scientist using PlasmoDB AI expression tools to explore the expression data associated with your gene if interest. Here are two gene expression summaries for the same gene, you must evaluate wich AI summary you find to more useful using the following criteria.\n"
        f"**CRITICAL INSTRUCTION:** Summary A uses the following criteria for scoring experiments:The AI was asked to rate the biological importance of each experimental result on a scale from 1 (least important) to 5 (most important).Each value in this column reflects the AI's predicted importance and confidence level—for example, 5A means the AI judged the result to be highly important with high confidence, while 1E suggests low importance and low confidence.\n"
        f"**CRITICAL INSTRUCTION:** Summary B uses the following criteria for scoring experiments:\n"
    
        f" **Biological_importance score**: Integer 0-5 scale (0 lowest, 5 highest)\n"
        f"  0= No meaningful change (FC percentile >50%)\n"
        f"  1= Small change (FC percentile <50% and >40%)\n"
        f"  2= Modest Change (FC percentile <40% and >30%)\n"
        f"  3= Substantial change (FC percentile <30% and >20%)\n"
        f"  4= Large change (FC percentile <20% and >10%)\n"
        f"  5= Exceptional change (FC percentile <10%)\n"

        f"**Confidence_score**: Integer 0-5 (0 lowest, 5 highest)\n"
        f"  N/A= No differential expression data available\n"
        f"  0= No statistical support: P value >0.05\n"
        f"  1= Low statistical support: P value <0.05 and >=0.01\n"
        f"  2= Adequate statistical support: P value <0.01 and >=0.001 b\n"
        f"  3= Moderate statistical support: P value <0.001 and >=0.0001\n"
        f"  4=Strong statistical support: P value <0.0001\n"
        f"  5= Exceptional statistical support: P value <0.00001\n"

        f"The summaries are given below and the criteria in which you must assess the summaries is given. Please note that summary B does not have access to mRNA stability data and should not be penalsied for this\n"
        f"Summary A:{summary_a}\n"
        f"Summary B:{summary_b}\n" 

        f"###Biological Content\n"

        f"##Observations:\n"
        f"**Observations** are factual statements about expression patterns (e.g., 'high expression after blood feeding', 'increased in salivary glands').\n"
        f"Only in A: list of factual observations about expression patterns found ONLY in Summary A. Give the total number of observations in summary A \n"
        f"Only in B: list of factual observations about expression patterns found ONLY in Summary B. Give the total number of observations in summary B \n"
        f"Both: list of factual observations found in BOTH summaries. Give the total number of observations in both\n"
        f"Contradictions: please list if any observations are contradictory across the studies. Give the total number of contradictions\n"
        
        
        f"###Insights:\n"
        f"**Insights** are interpretations or biological conclusions (e.g., 'likely involved in digestion', 'may play a role in immune response')\n"
        f"Only in A:list of biological insights/interpretations found ONLY in Summary A. Give the total number of insights in summary A\n"
        f"Only in B:list of biological insights/interpretations found ONLY in Summary B. Give the total number of insights in summary A\n"
        f"Both: list of biological insights/interpretations found in BOTH summaries.Give the total number of insights in both summaries\n"
        f"Contradictions: please list if any insights are contradictory across the studies. Give the total number of contradictions\n"

        f"##Qualitative Assessment\n"

        f"###Tone and Style:\n"
        f"Summary A:description of tone and writing style in Summary A\n"
        f"Summary B:description of tone and writing style in Summary B\n"
        f"Comparison:comparison of tones and styles (always refer to 'Summary A' and 'Summary B', never just 'A' or 'B')\n"
        f"Please state the name of the summary that has preferred tone and style \n"
        f"NOTE: Summary B is given in markdown and should not be penalised for this\n"

        f"###Technical Detail Level\n"
        f"Summary A: assessment of technical detail in Summary A\n"
        f"Summary B: assessment of technical detail in Summary B\n"
        f"Comparison: comparison of detail levels (always refer to 'Summary A' and 'Summary B', never just 'A' or 'B')\n"
        f"Please state the name of the summary that has preferred technical detail level \n"

        f"###Headline:\n"
        f"Summary A: linguistic assessment of the top-level headline field in Summary A (clarity, specificity, informativeness, professional tone) - NOT the per-topic headlines\n"
        f"Summary B: linguistic assessment of the top-level headline field in Summary B (clarity, specificity, informativeness, professional tone) - NOT the per-topic headlines\n"
        f"Comparison: comparison of the top-level headline styles and potential utility for biologists (always refer to 'Summary A' and 'Summary B', never just 'A' or 'B')\n"
        f"Please state the name of the summary that has preferred headline \n"

        f"##Overall Summary \n"
        f"Combining all of your findings, give an overall summary of what summary you think is best for a user of the PlasmoDB database when exploring the expression data of a gene of interest.\n"
        f"**OUTPUT** The output must be in markdown format\n")

def produce_report(gene, repeat_num):
    summary_a_path = f"plasmodb_summaries/{gene}_A.txt"
    summary_b_path = f"expression_summary/meta_analysis_{gene}.md"
    output_file = f"comparison_output/{gene}_comparison.md"
    with open(summary_a_path, "r", encoding="utf-8") as f:
        summary_a_text = f.read()
    with open(summary_b_path, "r", encoding="utf-8") as f:
        summary_b_text = f.read()

    prompt = compare_prompts(summary_a_text,summary_b_text)
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=6000,
        messages=[{"role": "user", "content": prompt}])
    result = message.content[0].text
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

def main():
    for gene in gene_list:
        for i in range(1,2):  #repeat three times for each gene
            produce_report(gene, repeat_num=i)
        print(f"Finished {gene}")

main()
        
