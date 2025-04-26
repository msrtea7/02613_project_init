#!/bin/sh
#BSUB -q c02613
#BSUB -J task10
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=30GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -o task10.out
#BSUB -e task10.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

nsys profile -o task10_prof python task9.py 20
nsys stats task20_prof.nsys-rep

exit 0