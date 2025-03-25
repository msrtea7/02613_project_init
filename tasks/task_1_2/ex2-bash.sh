#!/bin/bash
#BSUB -J ex1-2
#BSUB -q hpc
#BSUB -W 60
#BSUB -R "rusage[mem=2000MB]"
#BSUB -o ex3.out
#BSUB -e ex3.err
#BSUB -N -B
#BSUB -u "s204438@student.dtu.dk"
#BSUB -R "select[model == XeonGold6226R]"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
time python simulate.py 10
time python simulate.py 12
time python simulate.py 14
time python simulate.py 16
time python simulate.py 18
time python simulate.py 20

exit 0
