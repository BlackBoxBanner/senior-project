import json
import os
from PIL import Image
import torch
from torch.utils.data import Dataset


class DominantColorDataset(Dataset):
    def __init__(self, json_file, img_dir, transform=None):
        with open(json_file, "r") as f:
            self.data = json.load(f)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = os.path.join(self.img_dir, self.data[idx]["name"])
        image = Image.open(img_name).convert("RGB")
        colors = self.data[idx]["color"]
        primary = self.hex_to_rgb(colors["primary"])
        secondary = self.hex_to_rgb(colors["secondary"])
        accent = self.hex_to_rgb(colors["accent"])
        labels = (
            torch.tensor([primary, secondary, accent], dtype=torch.float32) / 255.0
        )  # Normalize labels

        if self.transform:
            image = self.transform(image)

        return image, labels

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
