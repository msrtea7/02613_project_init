# Update info

Apr 5 2025<br>
Junrui Li

**WARNING, not finished**

## Current problem with /task5/parallelSim.py

1. Should use Pool directly instead of ThreadPool, which is still locked by GIL
2. The file IO was assigned for each worker, which I think should be removed. The File IO is IO-intensive, and calculation is computation-intensive, which requiring different ways of optimization. We should separetely optimize each of them, so here in this code I think we'd focus on calculation optimization, where just like the template code: file IO, then assign tasks to each worker. Maybe we could optimize how we File IO in the coming weeks

## Shell parameter

I'am also not sure with this parameter for ISF

```
#BSUB -n 17
```

Like we did parallelism with multiprocessing is process-level. So as we specify that for example 64 workers in our code, which means we are about to assign 64 processes. So if we should specify the ```BSUB -n``` parameter to 64? Otherwise some of my "workers" will wait.

And I was thinking if we should use ```real time``` or ```cpu time``` from the result of ```time``` command when calculation speedup. If we use cpu time then I feel like its okay to specify less number in ```BSUB -n``` than the number of workers.

I haven't tried it our yet, since the program is running. 

