#!/bin/bash
#BSUB -J ex5-6
#BSUB -q hpc
#BSUB -W 400
#BSUB -R "rusage[mem=1000MB]"
#BSUB -R "select[model == XeonGold6226R]"
#BSUB -R "span[hosts=1]"
#BSUB -o ex56.out
#BSUB -e ex56.err
#BSUB -n 17
#BSUB -N 
#BSUB -B 
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Number of buildings to process
N_BUILDINGS=400

# Array of worker counts to test
WORKERS=(1 2 4 8 16)

# Loop through the three modes
for MODE in 0 1 2; do
    case $MODE in
        0) MODE_NAME="Static allocation with apply_async" ;;
        1) MODE_NAME="Static allocation with map and chunksize" ;;
        2) MODE_NAME="Dynamic allocation with map" ;;
    esac
    
    echo "=============================================="
    echo "Mode $MODE: $MODE_NAME"
    echo "=============================================="
    
    # Loop through different worker counts
    for N_WORKERS in "${WORKERS[@]}"; do
        echo "Testing with $N_WORKERS workers:"
        time python all_task56.py $N_BUILDINGS $N_WORKERS $MODE
        echo ""
    done
    
    echo ""
done

exit 0