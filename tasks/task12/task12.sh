#!/bin/bash
#BSUB -q c02613
#BSUB -J task8
#BSUB -W 150
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=30GB]"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -o task12.out
#BSUB -e task12.err
#BSUB -u "s204438@student.dtu.dk"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

SECONDS=0
lscpu
echo "============================================="
nvidia-smi
echo "============================================="
n=4571
echo "Running with n=$n"

echo "simulation_cuda.py"
python -u simulation_cuda.py $n
echo "Total job script time: ${SECONDS} s"

