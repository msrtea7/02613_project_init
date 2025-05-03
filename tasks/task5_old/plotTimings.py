import matplotlib.pyplot as plt
import numpy as np

def minSecToMin(min, sec):
    return min + sec / 60

x_workers = np.array([2, 4, 8, 16, 32])
y_4cores_basespeed = minSecToMin(6, 45.383)
y_4cores = np.array([
    y_4cores_basespeed/minSecToMin(4, 14.685), 
    y_4cores_basespeed/minSecToMin(3, 0.983), 
    y_4cores_basespeed/minSecToMin(3, 9.96), 
    y_4cores_basespeed/minSecToMin(5, 0.8)
])
y_16cores_basespeed = minSecToMin(6, 5.175)
y_16cores = np.array([
    y_16cores_basespeed/minSecToMin(3, 18.874), 
    y_16cores_basespeed/minSecToMin(2, 22.929), 
    y_16cores_basespeed/minSecToMin(1, 32.793), 
    y_16cores_basespeed/minSecToMin(2, 5.9)
])

y_16cores_many_buildings_basespeed = minSecToMin(19, 25.946)
y_16cores_many_buildings = np.array([
    y_16cores_many_buildings_basespeed/minSecToMin(11, 31.576), 
    y_16cores_many_buildings_basespeed/minSecToMin(7, 44.567), 
    y_16cores_many_buildings_basespeed/minSecToMin(5, 45.715), 
    y_16cores_many_buildings_basespeed/minSecToMin(5, 8.608),
    y_16cores_many_buildings_basespeed/minSecToMin(6, 8.762)
])

def plotTimings(x, y):
    plt.scatter(x, y, color='red')
    plt.title('100 buildings - 16 cores')
    plt.xlabel('No. of workers')
    plt.ylabel('Speedup (compared to 1 worker)')
    plt.show()

plotTimings(x_workers, y_16cores_many_buildings)