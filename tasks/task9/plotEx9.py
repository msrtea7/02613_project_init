import numpy as np
import matplotlib.pyplot as plt

N_values = [10, 12, 14, 16, 18, 20]
execution_times = [24.276, 32.022, 40.107, 45.096, 52.084, 59.469]

coefficients = np.polyfit(N_values, execution_times, 1)  

polynomial = np.poly1d(coefficients)

fitted_times = polynomial(N_values)

plt.figure(figsize=(8, 6))

plt.plot(N_values, execution_times, 'bo', label='Data (Execution Times)')

plt.plot(N_values, fitted_times, 'r-', label=f'Poly Fit: {polynomial}')

plt.xlabel('N (Input Size)', fontsize=12)
plt.ylabel('Execution Time (seconds)', fontsize=12)
plt.title('Execution Time vs. N with Polynomial Fit', fontsize=14)
plt.grid(True)
plt.xticks(N_values)  
plt.yticks(range(0, int(max(execution_times)) + 10, 5)) 

plt.legend()
plt.show()

print("Polynomial Coefficients: ", coefficients)
