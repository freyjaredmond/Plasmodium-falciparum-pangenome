## Create the job
#!/bin/bash
#SBATCH --job-name=lfof
#SBATCH --partition=med
#SBATCH --time=24-00:00:00
#SBATCH --mem=40G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --array=1-15
#SBATCH --output=job.%x.%A_%a.%N.out
#SBATCH --error=job.%x.%A_%a.%N.err



# Load / activate liftoff
module load liftoff/1.6.3


DATADIR="/mnt/hc-storage/users/freyja/get_pangenes/LiftOff"
GENOMEDIR="$DATADIR/Genome_data"
# File listing the 15 target genome directory names
targets_file="$DATADIR/targets_15.txt" #lists all the directories

# Old Genome
oldGenome=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$targets_file")


# Select target genome for this array task

newGenome="3D7"

# Genome assembly (unchanged) and the PSEUDO absent-gene annotation to lift genes from
oldGenome_asm="$GENOMEDIR/$oldGenome/${oldGenome}_Genome.fasta"
oldGenome_gff="$GENOMEDIR/$oldGenome/${oldGenome}_PSEUDO.gff"


# Target genome assembly to lift genes to

newGenome_asm="$GENOMEDIR/3D7/3D7_Genome.fasta"

# Create output directories

OUTDIR="$GENOMEDIR/$oldGenome/liftoff_out_PSEUDO"
mkdir -p "$OUTDIR"

INTERDIR="$OUTDIR/intermediate_dir_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
mkdir -p "$INTERDIR"


# Run liftoff

liftoff \
  "$newGenome_asm" \
  "$oldGenome_asm" \
  -g "$oldGenome_gff" \
  -o "$OUTDIR/${oldGenome}_liftover_no_flank_PSEUDO.gff3" \
  -u "$OUTDIR/${oldGenome}_liftover_unmapped_features_no_flank_PSEUDO.txt" \
  -exclude_partial \
  -dir "$INTERDIR" \
  -copies \
  -polish 
