from os.path import join
import sys
import numpy as np
import time
from numba import cuda


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


@cuda.jit
def jacobi_cuda_kernel(u, u_new, interior_mask):
    j, i = cuda.grid(2)

    # Add padding offset since u is (514, 514) and interior is (512, 512)
    if 1 <= i < u.shape[0] - 1 and 1 <= j < u.shape[1] - 1:
        if interior_mask[i - 1, j - 1]:
            u_new[i, j] = 0.25 * (u[i - 1, j] + u[i + 1, j] + u[i, j - 1] + u[i, j + 1])
        else:
            u_new[i, j] = u[i, j]  # Keep boundary or non-interior cells unchanged


def jacobi_cuda(u_host, interior_mask_host, max_iter):
    u_device = cuda.to_device(u_host)
    u_new_device = cuda.device_array_like(u_device)
    mask_device = cuda.to_device(interior_mask_host)

    tpb = (32, 32)
    bpg_x = (u_host.shape[0] + tpb[0] - 1) // tpb[0]
    bpg_y = (u_host.shape[1] + tpb[1] - 1) // tpb[1]
    blocks_per_grid = (bpg_x, bpg_y)

    for _ in range(max_iter):
        jacobi_cuda_kernel[blocks_per_grid, tpb](u_device, u_new_device, mask_device)
        u_device, u_new_device = u_new_device, u_device  # swap pointers

    return u_device.copy_to_host()


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
    all_u0 = cuda.pinned_array((N, 514, 514), dtype=np.float64)
    all_interior_mask = cuda.pinned_array((N, 512, 512), dtype=bool)
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    # warm up
    start = time.perf_counter()
    _ = jacobi_cuda(all_u0[0], all_interior_mask[0], 1)
    end = time.perf_counter()
    print(f"warm-up time: {(end - start):.3f} s")

    start = time.perf_counter()
    all_u = cuda.pinned_array_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_cuda(u0, interior_mask, MAX_ITER)
        all_u[i] = u
    end = time.perf_counter()
    print(f"execution time with N={N}: {(end - start):.3f} s")

    # Print summary statistics in CSV format
    stat_keys = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
    print("building_id," + ",".join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ",".join(str(stats[k]) for k in stat_keys))

    end0 = time.perf_counter()
    print(f"total time: {(end0 - start0):.3f} s")
