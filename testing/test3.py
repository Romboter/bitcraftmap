import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

fig, ax = plt.subplots(figsize=(8, 8))


colors = np.random.rand(8, 8)
print(colors)

# Hexagon size
hex_radius = 1
dx = 3/2 * hex_radius  # horizontal spacing
dy = np.sqrt(3) * hex_radius  # vertical spacing

# Plot an 8x8 grid of hexagons
for row in range(8):
    for col in range(8):
        # Offset every other row (odd-q layout)
        x = col * dx
        y = row * dy
        if col % 2 == 1:
            y += dy / 2  # stagger odd columns

        # Create hexagon
        hex = RegularPolygon(
            (x, y),
            numVertices=6,
            radius = hex_radius,
            orientation=np.radians(30),
            facecolor='lightblue', edgecolor='gray'
        )
        ax.add_patch(hex)

        # Label the hex with (row, col)
        ax.text(x, y, f'{row},{col}', ha='center', va='center', fontsize=8)

# Set limits and aspect
ax.set_xlim(-1, dx * 8)
ax.set_ylim(-1, dy * 8)
ax.set_aspect('equal')
ax.axis('off')
plt.show()