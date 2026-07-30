#swissprot download
wget https://ftp.ncbi.nlm.nih.gov/blast/db/swissprot.tar.gz

tar -xzvf swissprot.tar.gz

rm swissprot.tar.gz




#!/bin/bash
#SBATCH --job-name=blastp_babesia
#SBATCH --output=logs/blastp_%j.out        
#SBATCH --error=logs/blastp_%j.err         
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16                 
#SBATCH --mem=64G                          
#SBATCH --time=34:00:00                    
#SBATCH --partition=low

QUERY="/mnt/hc-storage/users/freyja/BLAST/random_100_babesia3.fasta"
DB="/mnt/hc-storage/users/freyja/BLAST/uniref90/uniref90"
OUTDIR="blast_results"
OUTFILE="${OUTDIR}/babesia_vs_uniref90_100(3).txt"
mkdir -p ${OUTDIR}
mkdir -p logs
module load ncbi-blast/2.12.0

blastp \
    -query ${QUERY} \
    -db ${DB} \
    -out ${OUTFILE} \
    -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle" \
    -evalue 1e-5 \
    -max_target_seqs 10 \
    -num_threads ${SLURM_CPUS_PER_TASK}