import os
import json
import numpy as np
import cv2
from PIL import Image

# Define input and output folders
json_folder = "./60-30-10/json"  # Path to JSON files
image_folder = "./60-30-10/image"  # Path to UI images
mask_output_folder = "./60-30-10/masks"  # Path to save binary masks

# Ensure mask output folder exists
os.makedirs(mask_output_folder, exist_ok=True)

# Process each JSON file
for json_file in os.listdir(json_folder):
    if not json_file.endswith(".json"):
        continue

    # Load JSON annotation
    json_path = os.path.join(json_folder, json_file)
    with open(json_path, "r") as f:
        data = json.load(f)

    # Get image file name and dimensions
    image_name = data["imagePath"]
    image_path = os.path.join(image_folder, image_name)

    if not os.path.exists(image_path):
        print(f"Warning: Image {image_name} not found, skipping...")
        continue

    image_width, image_height = data["imageWidth"], data["imageHeight"]

    # Create an empty mask (all zeros)
    mask = np.zeros((image_height, image_width), dtype=np.uint8)

    # Loop through annotations (objects)
    for shape in data["shapes"]:
        if shape["shape_type"] == "rectangle":  # Ensure it's a bounding box
            (x1, y1), (x2, y2) = shape["points"]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Fill mask with white color (255) for embedded images
            mask[y1:y2, x1:x2] = 255

    # Save the mask as PNG (same name as image)
    mask_filename = os.path.splitext(image_name)[0] + "_mask.png"
    mask_path = os.path.join(mask_output_folder, mask_filename)

    # Save mask image
    Image.fromarray(mask).save(mask_path)

    print(f"Saved mask: {mask_path}")

print("Mask generation completed!")
