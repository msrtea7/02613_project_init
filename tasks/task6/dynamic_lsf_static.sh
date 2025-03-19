#!/bin/bash
#BSUB -J temp_sim[1-24]    # 24tasks, indexing from 1-24
#BSUB -q hpc
#BSUB -W 30
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R "rusage[mem=3GB]"
#BSUB -n 8                 # usin 8 cores for signle task
#BSUB -R "span[hosts=1]"   
#BSUB -o ./res_chunk/chunk_task_%I.out       # %I, the task index
#BSUB -e ./res_chunk/chunk_task_%I.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613


TOTAL=4571                # all floors
CHUNKS=24                 # into 24 sub-tasks
PER_CHUNK=$((TOTAL / CHUNKS))
REMAINDER=$((TOTAL % CHUNKS))

# cal current task idx_start, idx_end
if [ $LSB_JOBINDEX -le $REMAINDER ]; then
    START=$(( (LSB_JOBINDEX-1) * (PER_CHUNK+1) ))
    END=$(( START + PER_CHUNK ))
else
    START=$(( (LSB_JOBINDEX-1) * PER_CHUNK + REMAINDER ))
    END=$(( START + PER_CHUNK - 1 ))
fi

echo "Job [ $LSB_JOBINDEX ] is Running on host: $(hostname)" >> ./res_chunk/hosts.txt


echo "Task $LSB_JOBINDEX started at: $(date)"
time python dynamic_chunk.py $START $END 8
echo "Task $LSB_JOBINDEX finished at: $(date)"