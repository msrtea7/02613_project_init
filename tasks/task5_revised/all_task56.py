from os.path import join
import sys
import numpy as np

# For dynamic scheduling
import multiprocessing as mp
# from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool

#  > ls -l |grep "^-"|wc -l
# or 
#  > ls /dtu/projects/02613_2025/data/modified_swiss_dwellings/ -lR|grep "^-"|wc -l
#  > 9143 = 4571*2 + 1

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)
    for _ in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq(1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior
        if delta < atol:
            break
    return u


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        "mean_temp": mean_temp,
        "std_temp": std_temp,
        "pct_above_18": pct_above_18,
        "pct_below_15": pct_below_15,
    }

def cal_temp_single(args):
    i, u0, interior_mask, MAX_ITER, ABS_TOL = args
    return i, jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)

def cal_temp_multiple(args_list):
    results = []
    for arg in args_list:
        i, u = cal_temp_single(arg)
        results.append((i, u))
    return results

if __name__ == "__main__":
    LOAD_DIR = "/dtu/projects/02613_2025/data/modified_swiss_dwellings/"

    with open(join(LOAD_DIR, "building_ids.txt"), "r") as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 4:
        print("Usage: python script.py <N_buildings> <N_process> <mode>")
        print("mode: 0 - Static allocation with apply_async")
        print("      1 - Static allocation with map and chunksize")
        print("      2 - Dynamic allocation with map")
        sys.exit(1)
    else:
        N = int(sys.argv[1])           # Number of buildings
        N_process = int(sys.argv[2])   # Number of processes
        mode = int(sys.argv[3])        # Allocation mode
        print(f"Processing {N} buildings with {N_process} processes using mode {mode}")
        print(f"Current CPU count: {mp.cpu_count()}")

    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype="bool")
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    
    # Prepare arguments for parallel processing
    args_list = [(i, all_u0[i], all_interior_mask[i], MAX_ITER, ABS_TOL) 
                for i in range(len(all_u0))]
    
    # Different parallelization strategies based on mode
    if mode == 0:
        # Static allocation with apply_async (similar to your previous code)
        chunk_size = int(np.ceil(len(args_list) / N_process))
        chunks = [args_list[i:i+chunk_size] for i in range(0, len(args_list), chunk_size)]
        
        with Pool(processes=N_process) as pool:
            results = []
            for chunk in chunks:
                # Each process gets a chunk of tasks to process
                results.append(pool.apply_async(cal_temp_multiple, (chunk,)))
            
            # Wait for all tasks to complete and collect results
            for result in results:
                chunk_results = result.get()
                for i, u in chunk_results:
                    all_u[i] = u
    
    elif mode == 1:
        # Static allocation with map and chunksize
        chunk_size = int(np.ceil(len(args_list) / N_process))
        with Pool(processes=N_process) as pool:
            for i, u in pool.map(cal_temp_single, args_list, chunksize=chunk_size):
                all_u[i] = u
    
    else:  # mode == 2 or any other value
        # Dynamic allocation with map (default small chunksize)
        with Pool(processes=N_process) as pool:
            for i, u in pool.map(cal_temp_single, args_list):
                all_u[i] = u

    # Print summary statistics in CSV format
    # stat_keys = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
    # print("building_id," + ",".join(stat_keys))  # CSV header
    # for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
    #     stats = summary_stats(u, interior_mask)
    #     print(f"{bid},", ",".join(str(stats[k]) for k in stat_keys))