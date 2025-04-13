#!/bin/bash
#BSUB -q c02613
#BSUB -J task8
#BSUB -W 30
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=30GB]"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -o output/task8_%J.out
#BSUB -e output/task8_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

SECONDS=0
lscpu
echo "============================================="
nvidia-smi
echo "============================================="
n=50
echo "Running with n=$n"

echo "simulation_cuda.py"
python -u simulation_cuda.py $n
echo "---------------------------------------------"
echo "simulation_cuda_no_branch.py"
python -u simulation_cuda_no_branch.py $n
echo "---------------------------------------------"
echo "Total job script time: ${SECONDS} s"

