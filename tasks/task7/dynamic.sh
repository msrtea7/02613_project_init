#!/bin/bash
#BSUB -J task_7
#BSUB -q hpc
#BSUB -W 60
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -o ./res/task_7_1000_8.out
#BSUB -e ./res/task_7_1000_8.err
#BSUB -B
#BSUB -N 

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

SECONDS=0
lscpu -C
echo "============================================="
n_p=8
echo "Running with n=$n_p"
# 1st arg: first N floors under building_ids.txt
# 2nd arg: n_processes
time python dynamic.py 10 16
echo "============================================="
echo "Total execution time: ${SECONDS}s"
