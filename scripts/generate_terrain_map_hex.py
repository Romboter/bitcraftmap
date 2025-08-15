import cv2
import numpy as np
import math

map_folder = 'assets/maps/'
data_folder = 'assets/data/'
terrain_map_file_png = 'TerrainMap.gwm.png'
terrain_map_file_hexagon = 'TerrainMap.hex.png'

hex_size = 10          # hex radius in output pixels
scale = 16              # output size multiplier

# Load image
img = cv2.imread(data_folder + terrain_map_file_png)
h, w = img.shape[:2]

# Output image
out_h, out_w = int(h * scale), int(w * scale)
result = np.zeros((out_h, out_w, 3), dtype=np.uint8)

dx = math.sqrt(3) * hex_size
dy = 1.5 * hex_size

for y in np.arange(0, out_h + dy, dy):
    for x in np.arange(0, out_w + dx, dx):
        offset = dx / 2 if int(y // dy) % 2 else 0
        cx = x + offset
        cy = y

        orig_x = int(cx / scale)
        orig_y = int(cy / scale)

        if 0 <= orig_x < w and 0 <= orig_y < h:
            color = tuple(int(c) for c in img[orig_y, orig_x])

            pts = []
            for i in range(6):
                angle = math.pi / 6 + math.pi / 3 * i  # pointy top
                px = int(cx + hex_size * math.cos(angle))
                py = int(cy + hex_size * math.sin(angle))
                pts.append([px, py])
            pts = np.array([pts], dtype=np.int32)

            cv2.fillPoly(result, pts, color)

# Save output
cv2.imwrite(data_folder + terrain_map_file_hexagon, result)