#!/bin/bash
#BSUB -J task_4
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=20GB]"
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -o task_4_%J.out
#BSUB -e task_4_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

SECONDS=0
lscpu -C
echo "============================================="
n=10
echo "Running with n=$n"
time kernprof -l -v simulation.py $n
echo "============================================="
echo "Total execution time: ${SECONDS}s"

