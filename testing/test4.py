import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

fig, ax = plt.subplots(figsize=(8, 8))

# Create 8x8 array with random values between 0 and 1
colors = np.random.rand(8, 8)

# Normalize colors to a colormap
cmap = plt.cm.viridis
norm = plt.Normalize(vmin=colors.min(), vmax=colors.max())

# Hex size and spacing
hex_radius = 1
dx = 3/2 * hex_radius
dy = np.sqrt(3) * hex_radius

# Plot hex grid
for row in range(8):
    for col in range(8):
        x = col * dx
        y = row * dy
        if col % 2 == 1:
            y += dy / 2

        value = colors[row, col]
        color = cmap(norm(value))

        hex = RegularPolygon(
            (x, y),
            numVertices=6,
            radius = hex_radius,
            orientation = np.radians(30),
            facecolor = color,
            edgecolor='gray'
        )
        ax.add_patch(hex)

        ax.text(x, y, f'{row},{col}', ha='center', va='center', fontsize=7, color='white')

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

# Axis settings
ax.set_xlim(-1, dx * 8)
ax.set_ylim(-1, dy * 8)
ax.set_aspect('equal')
ax.axis('off')
plt.show()
