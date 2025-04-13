#!/bin/bash
#BSUB -q hpc
#BSUB -J task7
#BSUB -W 30
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=30GB]"
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -o output/task7_%J.out
#BSUB -e output/task7_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

SECONDS=0
lscpu
echo "============================================="
n=50
echo "Running with n=$n"
echo "simulation_jit_parallel.py"
python -u simulation_jit_parallel.py $n
echo "---------------------------------------------"
echo "Total job script time: ${SECONDS} s"

