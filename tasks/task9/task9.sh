!/bin/sh
#BSUB -q c02613
#BSUB -J task9
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=30GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -o task9.out
#BSUB -e task9.err


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python task9.py 10
time python task9.py 12
time python task9.py 14
time python task9.py 16
time python task9.py 18
time python task9.py 20

exit 0
