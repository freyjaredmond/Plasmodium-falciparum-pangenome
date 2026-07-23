## This script parses the PlasmoDB scripts to allow GET_PANGENES to run successfuly ##
## This script was created by Luc and modified to include pseudogenes ##
from pathlib import Path
import os
import shutil


def main(args):
    input_gff = args.input_gff
    copied_gff = str(Path(input_gff).with_suffix(".bak.gff"))
    shutil.copy(input_gff, copied_gff)
    output_gff = str(Path(input_gff).with_suffix(".fixed.gff"))
    with open(input_gff) as inp, open(output_gff, "w") as out:
        for line in inp:
            # Keep comments, blank lines, FASTA sections intact
            if line.startswith("#") or line.strip() == "":
                out.write(line)
                continue

            # Split GFF columns
            parts = line.rstrip("\n").split("\t")

            if len(parts) >= 3:
                if parts[2] in ("protein_coding_gene", "pseudogene"):
                    parts[2] = "gene"
                elif parts[2] == "pseudogenic_transcript":
                    parts[2] = "mRNA"

              


            out.write("\t".join(parts) + "\n")

    # Replace original file with fixed file
    os.replace(output_gff, input_gff)

    print("Done. Converted protein_coding_gene → gene, preserving comments.")


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fix GFF file by converting protein_coding_gene to gene."
    )
    parser.add_argument(
        "--input_gff",
        type=str,
        help="Path to the input GFF file.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
