import matplotlib.pyplot as plt
import numpy as np

# Data preparation
processes = [1, 4, 8, 12, 16, 24, 32, 64]
speedup_mode0 = [1.00, 3.07, 4.85, 6.70, 8.13, 8.70, 9.02, 9.30]
speedup_mode1 = [1.00, 2.96, 5.01, 6.57, 8.05, 8.65, 8.84, 9.31]
speedup_mode2 = [1.00, 3.38, 5.58, 6.60, 8.47, 8.54, 9.02, 9.35]

# Create the figure and axis
plt.figure(figsize=(10, 6))

# Plot the lines with different colors and markers
plt.plot(
    processes,
    speedup_mode0,
    "b-o",
    linewidth=2,
    markersize=8,
    label="Static with apply_async",
)
plt.plot(
    processes,
    speedup_mode1,
    "r-s",
    linewidth=2,
    markersize=8,
    label="Static with map+chunk",
)
plt.plot(
    processes, speedup_mode2, "g-^", linewidth=2, markersize=8, label="Dynamic with map"
)

# Add ideal speedup line (linear scaling)
# plt.plot(processes, processes, 'k--', linewidth=1.5, label='Ideal Speedup')

# Setting the x-axis to log scale
plt.xscale("log", base=2)

# Set the labels and title
plt.xlabel("Number of Processes", fontsize=14)
plt.ylabel("Speedup", fontsize=14)
plt.title("Speedup vs Number of Processes", fontsize=16)

# Set grid
plt.grid(True, linestyle="--", alpha=0.7)

# Set x-axis ticks to match the actual data points
plt.xticks(processes, labels=[str(p) for p in processes])

# Add legend
plt.legend(fontsize=12)

# Add text annotation explaining the chart
plt.figtext(
    0.5,
    0.01,
    "Comparison of parallelization strategies with increasing process count",
    ha="center",
    fontsize=10,
)

# Improve layout
plt.tight_layout()

# Save the figure
plt.savefig("speedup_comparison.png", dpi=300)

# Show the plot
plt.show()
