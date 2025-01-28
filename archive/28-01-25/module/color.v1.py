from collections import Counter
from PIL import Image
from webcolors import rgb_to_hex
import numpy as np
from sklearn.cluster import KMeans


class ColorModule:
    def __init__(self, image_path: str):
        """
        Initialize the ColorModule with the path to the image.
        :param image_path: Path to the image file.
        """
        self.image_path = image_path
        self.get_dominant_color_count = 3

    def _load_image(self, resize_dim=(300, 300)):
        """
        Load the image and resize it for processing.
        :param resize_dim: Tuple (width, height) to resize the image.
        :return: A numpy array of the resized image's RGB pixels.
        """
        image = Image.open(self.image_path).convert("RGB")
        resized_image = image.resize(resize_dim)
        return np.array(resized_image)

    def _extract_all_colors(self, pixels):
        """
        Extract all colors from the image as a flattened list of RGB tuples.
        :param pixels: Numpy array of image pixels.
        :return: A flattened list of RGB tuples.
        """
        return pixels.reshape(-1, 3)

    def _get_dominant_colors(self, rgb_pixels, top_n=None):
        """
        Use k-means clustering to identify the top N dominant colors.
        :param rgb_pixels: Flattened list of RGB tuples.
        :param top_n: Number of dominant colors to extract.
        :return: A list of tuples (color, percentage).
        """
        if top_n is None:
            top_n = self.get_dominant_color_count

        # Apply k-means clustering
        kmeans = KMeans(n_clusters=top_n, random_state=0)
        kmeans.fit(rgb_pixels)

        # Extract cluster centers and their counts
        cluster_centers = np.round(kmeans.cluster_centers_).astype(int)
        labels, counts = np.unique(kmeans.labels_, return_counts=True)

        # Sort clusters by count (dominance)
        sorted_clusters = sorted(
            zip(cluster_centers, counts), key=lambda x: x[1], reverse=True
        )

        # Convert RGB tuples to HEX and calculate percentages
        total_pixels = len(rgb_pixels)
        dominant_colors = [
            (tuple(color), round(count / total_pixels * 100, 2))
            for color, count in sorted_clusters
        ]

        return dominant_colors

    def get_dominant_colors(self):
        """
        Get the dominant, secondary, and accent colors, sorted by their percentages.
        :return: A dictionary with keys 'dominant', 'secondary', and 'accent',
                and their respective color codes and percentages.
        """
        pixels = self._load_image()
        rgb_pixels = self._extract_all_colors(pixels)

        # Get top N dominant colors using k-means
        dominant_colors = self._get_dominant_colors(rgb_pixels)

        # Map colors to HEX and normalize percentages
        result = {
            "dominant": (
                {
                    "code": rgb_to_hex(dominant_colors[0][0]),
                    "weight": dominant_colors[0][1],
                }
                if len(dominant_colors) > 0
                else None
            ),
            "secondary": (
                {
                    "code": rgb_to_hex(dominant_colors[1][0]),
                    "weight": dominant_colors[1][1],
                }
                if len(dominant_colors) > 1
                else None
            ),
            "accent": (
                {
                    "code": rgb_to_hex(dominant_colors[2][0]),
                    "weight": dominant_colors[2][1],
                }
                if len(dominant_colors) > 2
                else None
            ),
        }

        return result
