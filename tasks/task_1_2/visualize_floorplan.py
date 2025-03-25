import numpy as np
import matplotlib.pyplot as plt


def plot_domain(data):
    loadWallIndices = np.where(data == 5)
    insideWallIndices = np.where(data == 25)
    otherIndices = np.where(data == 0)

    plt.scatter(loadWallIndices[0], loadWallIndices[1], color='purple', s=0.07)
    plt.scatter(insideWallIndices[0], insideWallIndices[1], color='yellow', s=0.07)
    plt.scatter(otherIndices[0], otherIndices[1], color='black', s=0.07)

    plt.show()

def plot_interior(data):
    interiorPoints = np.where(data == 1)
    outsidePoints = np.where(data == 0)

    plt.scatter(interiorPoints[0], interiorPoints[1], color='white', s=0.07)
    plt.scatter(outsidePoints[0], outsidePoints[1], color='black', s=0.07)

    plt.show()

LOAD_DIR = 'modified_swiss_dwellings/23_interior.npy'
data = np.load(LOAD_DIR)
plot_interior(data)
