from PIL import Image, ImageOps
import numpy as np
import requests
# import math
# import cv2

width = height = 2400
pixel_size = 8 

with open("TerrainMap.uncompressed", "rb") as f:
    data = f.read()

expected_size = width * height * pixel_size
if len(data) < expected_size:
    raise ValueError("File too small for expected image size.")
elif len(data) > expected_size:
    data = data[:expected_size]  # Trim padding if any

rgb_data = bytearray()
for i in range(0, len(data), pixel_size):
    b, g, r = data[i+1], data[i+2], data[i+3]
    rgb_data.extend([r, g, b]) 

img_array = np.frombuffer(rgb_data, dtype=np.uint8).reshape((height, width, 3))

# Crop was a good idea but leaflet transform rectangles map to squares...
# crop_factor = 1.1547005 # magic number
# crop_pixels = int(height / crop_factor)
# img_array = img_array[:crop_pixels, :]

img = Image.fromarray(img_array, 'RGB')
img = ImageOps.mirror(img)
img = img.rotate(180)

scale_factor = 3
img = img.resize((2400 * scale_factor, 2400 * scale_factor), resample=Image.NEAREST)

img.save('assets/maps/map_new.png')
img.show()


'''
image_path = "reconstructed_rgb_image.png"        # Your input image file
output_path = "reconstructed_rgb_image_hex.png"  # Output file
hex_size = 20                   # Radius of hexagons

# Load the image
img = cv2.imread(image_path)
h, w = img.shape[:2]

# Create a blank result image
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
cv2.imwrite(output_path, result)
'''