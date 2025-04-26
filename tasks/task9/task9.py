from os.path import join
import sys
import time
import cupy as cp  # <<<<<< REPLACE numpy with cupy

def load_data(load_dir, bid):
    SIZE = 512
    u = cp.zeros((SIZE + 2, SIZE + 2))
    u_np = cp.asarray(cp.load(join(load_dir, f"{bid}_domain.npy")))  # Load with cp.load
    u[1:-1, 1:-1] = u_np
    interior_mask_np = cp.asarray(cp.load(join(load_dir, f"{bid}_interior.npy")))
    return u, interior_mask_np

def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = u.copy()
    for _ in range(max_iter):
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = cp.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior
        if delta < atol:
            break
    return u

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean().item()
    std_temp = u_interior.std().item()
    pct_above_18 = (cp.sum(u_interior > 18) / u_interior.size * 100).item()
    pct_below_15 = (cp.sum(u_interior < 15) / u_interior.size * 100).item()
    return {
        "mean_temp": mean_temp,
        "std_temp": std_temp,
        "pct_above_18": pct_above_18,
        "pct_below_15": pct_below_15,
    }

if __name__ == "__main__":
    LOAD_DIR = "/dtu/projects/02613_2025/data/modified_swiss_dwellings/"
    # LOAD_DIR = "../../data/"

    start0 = time.perf_counter()
    with open(join(LOAD_DIR, "building_ids.txt"), "r") as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 4
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = cp.empty((N, 514, 514))
    all_interior_mask = cp.empty((N, 512, 512), dtype=cp.bool_)
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    start = time.perf_counter()
    all_u = cp.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u
    end = time.perf_counter()
    print(f"execution time with N={N}: {(end - start):.3f} s")

    # Print summary statistics in CSV format
    stat_keys = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
    print("building_id," + ",".join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid}," + ",".join(str(stats[k]) for k in stat_keys))

    end0 = time.perf_counter()
    print(f"total time: {(end0 - start0):.3f} s")
