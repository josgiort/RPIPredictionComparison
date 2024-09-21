#!/bin/bash
#SBATCH --job-name=matShow.job
#SBATCH --output=.out/matShow.out
#SBATCH --error=.out/matShow.err
#SBATCH --time=00:01:00
#SBATCH --mem=12000
#SBATCH --qos=normal
python $HOME/matShow.py
