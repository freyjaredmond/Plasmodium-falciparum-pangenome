
#!/bin/bash
#SBATCH --job-name=PanGenes_Growth_v2
#SBATCH --partition=low
#SBATCH --output=/mnt/hc-storage/users/freyja/get_pangenes/log_files/pangenes_growth_v2_%j.log
#SBATCH --error=/mnt/hc-storage/users/freyja/get_pangenes/err_files/pangenes_growth_v2_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=200:00:00

module purge

export PATH="/mnt/hc-storage/users/freyja/micromamba/envs/get_pangenes/bin:$PATH"

PROJ="/mnt/hc-storage/users/freyja/get_pangenes"
GETP="/mnt/hc-storage/users/freyja/micromamba/envs/get_pangenes/bin/get_pangenes.pl"
PY="/mnt/hc-storage/users/freyja/micromamba/envs/get_pangenes/bin/python"

HELPER="$PROJ/get_pangenes_pseudo.py"
SOURCE_DIR="$PROJ/inputs_pseudo"
INPUT_DIR="$PROJ/inputs_pseudo_single"
BACKUP_DIR="$PROJ/inputs_pseudo_single_backups"

mkdir -p "$PROJ/log_files" "$PROJ/err_files" "$INPUT_DIR" "$BACKUP_DIR"

# Copy gffs and fasta into a new folder
cp "$SOURCE_DIR"/*.gff "$SOURCE_DIR"/*.fasta "$INPUT_DIR"/

# convert gffs using the helper script
for gff in "$INPUT_DIR"/*.gff; do
  "$PY" "$HELPER" --input_gff "$gff"
done

# Remove backups from previous run
find "$INPUT_DIR" -maxdepth 1 -type f -name "*.bak*.gff" -exec mv {} "$BACKUP_DIR"/ \;

# Run pangenes, excluding singletons
"$GETP" -d "$INPUT_DIR" -t 0 -c -t 2
