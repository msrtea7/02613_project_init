import numpy as np
import matplotlib.pyplot as plt

# Define the N values and the corresponding execution times (in seconds)
N_values = [10, 12, 14, 16, 18, 20]
execution_times = [24.276, 32.022, 40.107, 45.096, 52.084, 59.469]

# Perform a polynomial fit (2nd degree polynomial for example)
coefficients = np.polyfit(N_values, execution_times, 1)  # Fit a 2nd degree polynomial

# Generate the fitted polynomial function
polynomial = np.poly1d(coefficients)
print(polynomial)

# Generate fitted values using the polynomial function
fitted_times = polynomial(N_values)

# Create the plot
plt.figure(figsize=(8, 6))

# Plot the original data points
plt.plot(N_values, execution_times, 'bo', label='Data (Execution Times)')

# Plot the polynomial fit line
plt.plot(N_values, fitted_times, 'r-', label=f'Poly Fit: {polynomial}')

# Add labels and title
plt.xlabel('N (Input Size)', fontsize=12)
plt.ylabel('Execution Time (seconds)', fontsize=12)
plt.title('Execution Time vs. N with Polynomial Fit', fontsize=14)
plt.grid(True)
plt.xticks(N_values)  # Ensure each N value is marked on the x-axis
plt.yticks(range(0, int(max(execution_times)) + 10, 5))  # Set y-axis tick spacing

# Show the legend
plt.legend()

# Show the plot
plt.show()

# Print the polynomial coefficients
print("Polynomial Coefficients: ", coefficients)
