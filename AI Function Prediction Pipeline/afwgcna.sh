#!/bin/bash -l
#SBATCH -J alphafold3
#SBATCH -o alphafold3_%A_%a.out
#SBATCH -e alphafold3_%A_%a.err
#SBATCH -p gpu
#SBATCH --ntasks-per-node=1
#SBATCH -c 32
#SBATCH --gres=gpu:1
#SBATCH -t 3-00:00:00
#SBATCH --mail-user=freyja@liverpool.ac.uk
#SBATCH --mail-type=ALL
#SBATCH --array=1-200
#SBATCH --exclude=compute36

# NOTE: module load singularity/3.8.6 removed - that module points to an old
# SingularityCE 3.8.6 install requiring setuid, which is broken on this cluster.
# The system default (/usr/bin/singularity -> Apptainer 1.5.2) works fine and
# is used automatically without loading any module.

# make a unique tmp directory per array task to avoid cross-task collisions
TMPDIR_TASK=/mnt/hc-storage/users/freyja/alphafold3/alphafold3_output/tmp/${SLURM_ARRAY_TASK_ID}
mkdir -p ${TMPDIR_TASK}

#file containing the json names
FILE=`sed -n ${SLURM_ARRAY_TASK_ID}p /mnt/hc-storage/users/freyja/alphafold3/WGCNA_wgcna_test_json.txt`

singularity exec \
     --nv \
     --bind /mnt/hc-storage/users/freyja/alphafold3/af3_wgcna_input/WGCNA_jsons:/root/af_input \
     --bind /mnt/hc-storage/users/freyja/alphafold3/af3_wgcna_output:/root/af_output \
     --bind /mnt/hc-storage/users/freyja/alphafold3/model_parameters:/root/models \
     --bind /mnt/hc-storage/alphafold3_databases/public_databases:/root/public_databases \
     --bind ${TMPDIR_TASK}:/tmp \
     --env XLA_PYTHON_CLIENT_PREALLOCATE=false,TF_FORCE_UNIFIED_MEMORY=true,XLA_CLIENT_MEM_FRACTION=3.2 \
     /mnt/hc-storage/containers/alphafold3.sif \
     python /app/alphafold/run_alphafold.py \
     --json_path=/root/af_input/${FILE} \
     --model_dir=/root/models \
     --db_dir=/root/public_databases \
     --pdb_database_path=/root/public_databases/mmcif_files \
     --output_dir=/root/af_output
