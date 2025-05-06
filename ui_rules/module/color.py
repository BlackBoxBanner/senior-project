from __future__ import annotations
import base64
from io import BytesIO
from typing import Any, Tuple, List

import cv2
import numpy as np
from numpy.typing import NDArray
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class ColorModule:
    @staticmethod
    def load_image(path: str) -> NDArray[np.uint8]:
        """Load an image from a file path as an RGB numpy array."""
        with Image.open(path) as img:
            return np.array(img.convert("RGB"))

    @staticmethod
    def load_base64_image(base64_str: str) -> NDArray[np.uint8]:
        """Decode base64 string into an RGB image array."""
        decoded = base64.b64decode(base64_str)
        with Image.open(BytesIO(decoded)) as img:
            return np.array(img.convert("RGB"))

    @staticmethod
    def resize_image(image: NDArray[np.uint8], size: Tuple[int, int]) -> NDArray[Any]:
        """Resize image using OpenCV."""
        return cv2.resize(image, size)

    @staticmethod
    def remove_background(image: NDArray[np.uint8]) -> NDArray[Any]:
        """Remove background using binary thresholding on grayscale."""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        return cv2.bitwise_and(image, image, mask=mask)

    @staticmethod
    def extract_dominant_colors(
        image: NDArray[np.uint8], color_number: int = 3
    ) -> List[Tuple[List[int], int]]:
        """Extract dominant non-black RGB colors with their pixel counts."""
        pixels = image.reshape(-1, 3)
        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

        if pixels.size == 0:
            raise ValueError("No non-black pixels found.")

        kmeans = KMeans(n_clusters=color_number, n_init="auto", random_state=42)
        kmeans.fit(pixels)

        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        return [
            (kmeans.cluster_centers_[label].astype(int).tolist(), int(count))
            for label, count in zip(labels, counts)
        ]

    @staticmethod
    def calculate_percentages(
        colors: List[Tuple[List[int], int]]
    ) -> List[Tuple[List[int], int]]:
        """Convert counts to percentage and sort descending."""
        total = sum(count for _, count in colors)
        percentages = [
            (color, round((count / total) * 100)) if total > 0 else (color, 0)
            for color, count in colors
        ]
        return sorted(percentages, key=lambda x: x[1], reverse=True)

    @staticmethod
    def plot_colors(colors: List[Tuple[List[int], int]]) -> None:
        """Visualize dominant colors as a horizontal bar chart."""
        if not colors:
            print("No colors to plot.")
            return

        fig, ax = plt.subplots(figsize=(8, 2))
        start = 0
        for rgb, percent in colors:
            color = np.array(rgb) / 255
            ax.barh(0, width=percent, left=start, color=color, edgecolor="black")
            start += percent

        ax.set_xlim(0, 100)
        ax.axis("off")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def save_colors(colors: List[Tuple[List[int], int]], filepath: str) -> None:
        """Save RGB and percentage values to a text file."""
        with open(filepath, "w") as f:
            for color, percent in colors:
                f.write(f"Color RGB{tuple(color)} - {percent}%\n")

    @staticmethod
    def hex_from_rgb(rgb: List[int]) -> str:
        """Convert RGB list to hex string."""
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def hex_colors(self, colors: List[Tuple[List[int], int]]) -> List[Tuple[str, int]]:
        """Convert list of RGB colors to HEX with percentages."""
        return [(self.hex_from_rgb(color), percent) for color, percent in colors]

    @staticmethod
    def srgb_to_linear(component: float) -> float:
        """Convert an sRGB component to linear light."""
        c = component / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def relative_luminance(self, r: int, g: int, b: int) -> float:
        """Calculate relative luminance of an sRGB color."""
        R, G, B = map(self.srgb_to_linear, [r, g, b])
        return 0.2126 * R + 0.7152 * G + 0.0722 * B

    def contrast_ratio(self, color1: List[int], color2: List[int]) -> float:
        """Calculate contrast ratio between two RGB colors."""
        L1 = self.relative_luminance(*color1)
        L2 = self.relative_luminance(*color2)
        lighter, darker = max(L1, L2), min(L1, L2)
        return round((lighter + 0.05) / (darker + 0.05), 2)