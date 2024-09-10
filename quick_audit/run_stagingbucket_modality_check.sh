#!/bin/bash -l
#SBATCH --job-name=modalitycheck
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=60gb
#SBATCH --output=logs/modalitycheck_%A_%a.out
#SBATCH --error=logs/modalitycheck_%A_%a.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -A miran045

mkdir logs
source /home/faird/shared/code/external/envs/miniconda3/load_miniconda3.sh
python3 stagingbucket_filecheck.py
