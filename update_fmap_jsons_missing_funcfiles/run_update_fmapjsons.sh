#!/bin/bash -l
#SBATCH --job-name=fixjsons
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=60gb
#SBATCH --output=/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/logs/fixjsons_%A_%a.out
#SBATCH --error=/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/logs/fixjsons_%A_%a.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -A elisonj

source /home/faird/shared/code/external/envs/miniconda3/load_miniconda3.sh
python3 update_fmap_jsons.py
