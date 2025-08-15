from PIL import Image, ImageOps
import numpy as np
import requests
import gzip
import shutil
import math
import cv2

width = 2400
height = 2400
pixel_size = 8 
scale_factor = 3
header_size = 8
hex_size = 6
expected_size = width * height * pixel_size

maps_url = 'https://maps.game.bitcraftonline.com/world-maps/'
terrain_map_file = 'TerrainMap.gwm'
terrain_map_file_unzip = 'TerrainMap.gwm.unc'
terrain_map_file_png = 'TerrainMap.gwm.png'
terrain_map_file_hexagon = 'TerrainMap.hex.png'
data_folder = 'assets/data/'
map_folder = 'assets/maps/'

# Download and unzip the terrain map file
response = requests.get(maps_url + terrain_map_file, stream=True)
response.raise_for_status()

with open(data_folder + terrain_map_file, "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            file.write(chunk)

with gzip.open(data_folder + terrain_map_file, "rb") as f_in:
    with open(data_folder + terrain_map_file_unzip, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

# Read the uncompressed terrain map file and convert it to PNG format
with open(data_folder + terrain_map_file_unzip, "rb") as f:
    data = f.read()

pixel_data = data[header_size:]

if len(pixel_data) < expected_size:
    raise ValueError("File too small for expected image size.")
elif len(pixel_data) > expected_size:
    pixel_data = pixel_data[:expected_size]  # Trim padding if any

rgb_data = bytearray()
for i in range(0, len(pixel_data), pixel_size):
    b, g, r = pixel_data[i+1], pixel_data[i+2], pixel_data[i+3]
    rgb_data.extend([r, g, b]) 

img_array = np.frombuffer(rgb_data, dtype=np.uint8).reshape((height, width, 3))

img = Image.fromarray(img_array)
img = ImageOps.mirror(img)
img = img.rotate(180)
img = img.resize((2400 * scale_factor, 2400 * scale_factor), resample=Image.NEAREST)

img.save(data_folder + terrain_map_file_png)
#img.show()

# From square pixels to hexagonal pixels
img = cv2.imread(data_folder + terrain_map_file_png)
h, w = img.shape[:2]
result = np.zeros_like(img)

# Hexagon geometry
dx = hex_size * 3 / 2
dy = hex_size * math.sqrt(3)

# Loop through the image with hex centers
for y in np.arange(0, h + dy, dy):
    for x in np.arange(0, w + dx, dx):
        offset = (hex_size * 3/4) if int(y // dy) % 2 else 0
        cx = int(x + offset)
        cy = int(y)

        # Skip if center is outside the image
        if cx < 0 or cx >= w or cy < 0 or cy >= h:
            continue

        # Compute 6-point hexagon around (cx, cy)
        pts = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = int(cx + hex_size * math.cos(angle))
            py = int(cy + hex_size * math.sin(angle))
            pts.append([px, py])
        pts = np.array([pts], dtype=np.int32)

        # Create a mask for the hexagon
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, pts, 255)

        # Average color inside the hexagon
        mean_color = cv2.mean(img, mask=mask)
        color = tuple(map(int, mean_color[:3]))

        # Fill the hexagon in the result image
        cv2.fillPoly(result, pts, color)

# Save the output image
cv2.imwrite(data_folder + terrain_map_file_hexagon, result)