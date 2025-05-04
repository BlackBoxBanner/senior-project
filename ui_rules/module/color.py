import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import base64
from io import BytesIO


class ColorModule:
    def load_image(self, path: str) -> NDArray:
        """
        Load an image from a file and convert it to a numpy array with RGB format.
        """
        img = Image.open(path).convert("RGB")
        return np.array(img)

    def load_base64_image(self, base64_str: str) -> NDArray:
        """
        Load an image from a base64 string and convert it to a numpy array with RGB format.
        """
        img = base64.b64decode(base64_str)
        img = BytesIO(img)
        img = Image.open(img).convert("RGB")
        return np.array(img)

    def resize_image(self, img: NDArray, size: tuple[int, int]) -> NDArray:
        """
        Resize an image to the specified size.
        """
        return cv2.resize(img, size)

    def remove_background(self, image: NDArray) -> NDArray:
        """
        Remove background by thresholding on grayscale image.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        return cv2.bitwise_and(image, image, mask=mask)

    def extract_dominant_colors(
        self, image: NDArray, color_number: int = 3
    ) -> list[tuple[list[int], int]]:
        """
        Extract the most dominant colors (ignoring black pixels).
        Returns:
            A list of tuples: (RGB color as list[int], pixel count as int)
        """
        pixels = image.reshape(-1, 3)
        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

        if len(pixels) == 0:
            raise ValueError("No non-black pixels found in the image.")

        kmeans = KMeans(n_clusters=color_number, n_init="auto", random_state=42)
        kmeans.fit(pixels)

        colors, counts = np.unique(kmeans.labels_, return_counts=True)

        dominant_colors: list[tuple[list[int], int]] = [
            (kmeans.cluster_centers_[i].astype(int).tolist(), int(counts[i]))
            for i in range(len(colors))
        ]
        return dominant_colors

    def check_percent(
        self, colors: list[tuple[list[int], int]]
    ) -> list[tuple[list[int], int]]:
        """
        Convert raw pixel counts to percentages and sort by percentage descending.
        """
        total = sum(count for _, count in colors)
        if total == 0:
            sorted_colors = [(color, 0) for color, _ in colors]
        else:
            sorted_colors = [
                (color, round((count / total) * 100)) for color, count in colors
            ]

        sorted_colors.sort(key=lambda x: x[1], reverse=True)
        return sorted_colors

    def plot_colors(self, colors: list[tuple[list[int], int]]) -> None:
        """
        Plot the dominant colors as a horizontal bar.
        """
        if not colors:
            print("No colors to plot.")
            return

        color_patches = [np.array(color) / 255 for color, _ in colors]
        percentages = [percent for _, percent in colors]

        fig, ax = plt.subplots(figsize=(8, 2))
        start = 0

        for color, percent in zip(color_patches, percentages):
            ax.barh(0, width=percent, left=start, color=color, edgecolor="black")
            start += percent

        ax.set_xlim(0, 100)
        ax.axis("off")
        plt.show()

    def save_colors(self, colors: list[tuple[list[int], int]], filepath: str) -> None:
        """
        Save the dominant colors and their percentages to a text file.
        """
        with open(filepath, "w") as f:
            for color, percent in colors:
                f.write(f"Color RGB{tuple(color)} - {percent}%\n")

    def hex_from_rgb(self, rgb: list[int]) -> str:
        """
        Convert an RGB list to a hex string.
        """
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def hex_colors(self, colors: list[tuple[list[int], int]]) -> list[tuple[str, int]]:
        """
        Return a list of (hex_color, percentage) from (rgb_color, percentage).
        """
        return [(self.hex_from_rgb(color), percent) for color, percent in colors]

    def srgb_to_linear(self, component: float):
        """Convert an sRGB component (0-255) to linear space."""
        component = component / 255.0
        if component <= 0.03928:
            return component / 12.92
        else:
            return ((component + 0.055) / 1.055) ** 2.4

    def relative_luminance(self, r: int, g: int, b: int):
        """Calculate the relative luminance of an sRGB color."""
        R = self.srgb_to_linear(r)
        G = self.srgb_to_linear(g)
        B = self.srgb_to_linear(b)
        return 0.2126 * R + 0.7152 * G + 0.0722 * B

    def contrast_ratio(self, color1: list[int], color2: list[int]):
        """
        Calculate contrast ratio between two colors.
        Each color is a tuple of (R, G, B) in 8-bit sRGB.
        """
        L1 = self.relative_luminance(*color1)
        L2 = self.relative_luminance(*color2)
        lighter = max(L1, L2)
        darker = min(L1, L2)
        return round((lighter + 0.05) / (darker + 0.05), 2)
