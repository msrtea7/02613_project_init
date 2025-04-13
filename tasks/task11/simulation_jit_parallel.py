from os.path import join
import sys
import numpy as np
import time
import numba


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


@numba.njit(parallel=True, cache=False)
def jacobi(u, interior_coords, max_iter, atol=1e-6):
    u = u.copy()
    u_new = u.copy()
    n_coords = interior_coords.shape[0]

    for _ in range(max_iter):
        delta_array = np.zeros(n_coords)  # Used to record the error at each point in parallel

        for k in numba.prange(n_coords):
            i = interior_coords[k, 0] + 1
            j = interior_coords[k, 1] + 1
            val = 0.25 * (u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1])
            diff = abs(u[i, j] - val)
            delta_array[k] = diff
            u_new[i, j] = val

        delta = delta_array.max()
        if delta < atol:
            return u_new

        u, u_new = u_new, u

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
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype="bool")
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    start = time.perf_counter()
    all_u = np.empty_like(all_u0)
    all_interior_coords = []
    for mask in all_interior_mask:
        coords = np.array(np.where(mask)).T
        coords = coords[np.lexsort((coords[:, 1], coords[:, 0]))]  # row-major sort
        all_interior_coords.append(coords)

    # warm-up
    start = time.perf_counter()
    _ = jacobi(all_u0[0], all_interior_coords[0], 1, ABS_TOL)
    end = time.perf_counter()
    print(f"warm-up time: {(end - start):.3f} s")

    for i, (u0, interior_coords) in enumerate(zip(all_u0, all_interior_coords)):
        u = jacobi(u0, interior_coords, MAX_ITER, ABS_TOL)
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
