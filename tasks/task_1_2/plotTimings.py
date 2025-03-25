import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

x = np.array([10, 12, 14, 16, 18, 20])
y = np.array([1+17/60, 1+44/60, 2+14/60, 2+28/60, 2+47/60, 3+14/60])
a,b = np.polyfit(x, y, 1) # fit to points

def f(k):    
    return a*k+b

# print fitted function 
print("f(x) = {a} * x + {b}".format(a = np.round(a, 3), b = np.round(b, 3)))
plt.scatter(x, y, color='red')
plt.plot(x, f(np.array(x)), color='blue')

legend_lines = [Line2D([0], [0], color='red', lw=2), 
                Line2D([0], [0], color='blue', lw=2)]    


fx = "f(x) ≈ {a} * x + {b}".format(a = np.round(a, 3), b = np.round(b, 3))
plt.legend(legend_lines, ['Measured time taken', fx], loc='upper left')
print(f(4571))
plt.xlabel('No. of floorplans simulated')
plt.ylabel('Time taken (min) (real time)')
plt.show()