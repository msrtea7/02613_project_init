#!/bin/sh
#BSUB -q c02613
#BSUB -J task10fix
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=30GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -o task10fix.out
#BSUB -e task10fix.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

nsys profile -o task10fix_prof python task10fix.py 20
nsys stats task10fix_prof.nsys-rep

exit 0