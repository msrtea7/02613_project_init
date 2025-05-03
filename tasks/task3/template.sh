#!/bin/bash
#BSUB -J task_1
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=20GB]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o task_1_%J.out
#BSUB -e task_1_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

SECONDS=0
lscpu
echo "============================================="
n=5
echo "Running with n=$n"
time python -u simulation.py $n
echo "============================================="
echo "Total execution time: ${SECONDS}s"

