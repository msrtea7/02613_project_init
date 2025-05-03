#!/bin/bash
#BSUB -J ex1-2
#BSUB -q hpc
#BSUB -W 400
#BSUB -R "rusage[mem=1000MB]"
#BSUB -o ex3.out
#BSUB -e ex3.err
#BSUB -N -B
#BSUB -u "s204438@student.dtu.dk"
#BSUB -R "select[model == XeonGold6226R]"
#BSUB -n 4
#BSUB -R "span[hosts=1]"
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
echo "1 worker:"
time python parallelSim.py 1

echo "2 workers:"
time python parallelSim.py 2

echo "4 workers:"
time python parallelSim.py 4

echo "8 workers:"
time python parallelSim.py 8

echo "16 workers:"
time python parallelSim.py 16

echo "32 workers:"
time python parallelSim.py 32

echo "64 workers:"
time python parallelSim.py 64

exit 0
