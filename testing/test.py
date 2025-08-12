import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.colors import ListedColormap


#A = np.random.random((10, 10))
#print(A)

array = [
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10],
        [1,2,3,4,5,6,7,8,9,10]
    ]

A = np.array(array)



X, Y = np.meshgrid(range(A.shape[0]), range(A.shape[-1]))

print(X)
print(Y)
X, Y = X*2, Y*2


print(X)
print(Y)

# Turn this into a hexagonal grid
for i, k in enumerate(X):
    if i % 2 == 1:
        X[i] += 1
        Y[:,i] += 1


print(X)
print(Y)

fig, ax = plt.subplots()
im = ax.hexbin(
    X.reshape(-1), 
    Y.reshape(-1), 
    C=A.reshape(-1), 
    gridsize=int(A.shape[0]/2)
)

# the rest of the code is adjustable for best output
ax.set_aspect(0.8)
ax.set(xlim=(-4, X.max()+4,), ylim=(-4, Y.max()+4))
ax.axis(False)
plt.show()