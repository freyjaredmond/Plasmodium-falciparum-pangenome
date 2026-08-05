import os
from dotenv import load_dotenv
import anthropic
import glob

# Load environment variables
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def score_prompt(summary, keywords):
    return (
        f"You are a scientist investigating whether the terms used by an AI expression summary actually reflect the underlying RNA-seq data \n"
        f"The following contains several AI expression summaries for individual RNA-seq experiments for a gene of interest:\n{summary}\n"
        f" You are also provided with the following score mapping table:\n{keywords}\nThis table gives keywords that should reflect the magnitude of change \n"
        f" A score of 5 is a dramatic change amongst at least one comparison, whereas a score of 0 is no change amongst comparisons \n"
        f" The change can be up or downregulated \n"
        f" IMPORTANT: You are scoring the MAGNITUDE OF CHANGE across conditions, not the level of expression. "
        f"A gene described as 'highly expressed' or 'abundantly present' but showing NO change across conditions must score 0 or N/A — high baseline expression does not justify a high score. "
        f"Only keywords describing a DIFFERENCE between conditions (e.g. increased, upregulated, elevated) should drive the score. \n"
        f" Your task is to rate each experiment based on the magnitude of change described using the keywords in the table \n"
        f" You must score the language, not the data being presented \n"
        f" If you believe that only baseline expression and not change is described, score this N/A \n"
        f" If you think one summary overlaps two scores you may report the score as 4/5 for example \n"
         f"Output: a TSV with columns: study, score, explanation (one sentence explaining the score).\n"
        f"Output the TSV only — no preamble, no analysis, no markdown formatting or code blocks. The first line must be the header row.\n")



#gene_list = [
    "PF3D7_0420100", "PF3D7_1352100", "PF3D7_1470700", "PF3D7_1313800", "PF3D7_1117700",
    "PF3D7_0423700", "PF3D7_1108500", "PF3D7_1032400", "PF3D7_0607300", "PF3D7_0710900",
#]
gene_list=["PF3D7_0423700"]


def produce_report(gene):
    summary_path = f"studies_keywords/{gene}.txt"
    keywords = f"scoring_keywords.tsv"
    output_file = f"keywords_scored/{gene}_scored.tsv"

    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()
    with open(keywords, "r", encoding="utf-8") as f:
        threshold_text = f.read()


    prompt = score_prompt(summary_text, threshold_text)
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=6000,
        messages=[{"role": "user", "content": prompt}])
    result = message.content[0].text
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

def main():
    for gene in gene_list:
        produce_report(gene)
        print(f"Finished {gene}")

main()