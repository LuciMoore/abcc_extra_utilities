#!/bin/bash -l
#SBATCH --job-name=dtype
#SBATCH --time=2:00:00
#SBATCH --mem-per-cpu=80gb
#SBATCH --tmp=40gb
#SBATCH --output=output_logs/dicom2bids_%A_%a.out
#SBATCH --error=output_logs/dicom2bids_%A_%a.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -A elisonj
#SBATCH -p aglarge,agsmall

cd run_files.no_s3
file=run${SLURM_ARRAY_TASK_ID}
bash ${file}
