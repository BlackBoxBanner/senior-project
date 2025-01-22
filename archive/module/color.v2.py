from collections import Counter
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


class ColorModule:
    def __init__(self, image_path: str, num_colors: int = 3):
        """
        Initialize the ColorModule with the path to the image and the number of dominant colors to extract.
        :param image_path: Path to the image file.
        :param num_colors: Number of dominant colors to extract (default is 3).
        """
        self.image_path = image_path
        self.num_colors = num_colors

    def _load_image(self, resize_dim=(300, 300)):
        """
        Load the image and resize it for processing.
        :param resize_dim: Tuple (width, height) to resize the image.
        :return: A numpy array of the resized image's RGB pixels.
        """
        try:
            image = Image.open(self.image_path).convert("RGB")
            resized_image = image.resize(resize_dim)
            return np.array(resized_image)
        except Exception as e:
            raise ValueError(f"Failed to load image: {e}")

    @staticmethod
    def _rgb_to_hex(rgb):
        """
        Convert an RGB tuple to a HEX color code.
        :param rgb: Tuple representing an RGB color (e.g., (255, 0, 0)).
        :return: HEX color code as a string (e.g., '#FF0000').
        """
        return "#%02x%02x%02x" % rgb

    def _extract_all_colors(self, pixels):
        """
        Extract all colors from the image as a flattened list of RGB tuples.
        :param pixels: Numpy array of image pixels.
        :return: A flattened list of RGB tuples.
        """
        return pixels.reshape(-1, 3)

    def _get_dominant_colors(self, rgb_pixels):
        """
        Use k-means clustering to identify the top N dominant colors.
        :param rgb_pixels: Flattened list of RGB tuples.
        :return: A list of tuples (color, percentage).
        """
        if len(rgb_pixels) < self.num_colors:
            raise ValueError(
                "Number of unique colors in the image is less than the required number of clusters."
            )

        # Apply k-means clustering
        kmeans = KMeans(n_clusters=self.num_colors, random_state=0, n_init="auto")
        kmeans.fit(rgb_pixels)

        # Extract cluster centers and their counts
        cluster_centers = np.round(kmeans.cluster_centers_).astype(int)
        labels, counts = np.unique(kmeans.labels_, return_counts=True)

        # Sort clusters by count (dominance)
        total_pixels = len(rgb_pixels)
        dominant_colors = [
            (tuple(color), round(count / total_pixels * 100, 2))
            for color, count in sorted(
                zip(cluster_centers, counts), key=lambda x: x[1], reverse=True
            )
        ]

        return dominant_colors

    def get_dominant_colors(self):
        """
        Get the dominant, secondary, and accent colors, sorted by their percentages.
        :return: A dictionary with keys 'dominant', 'secondary', and 'accent',
                 and their respective color codes and percentages.
        """
        # Step 1: Load and process the image
        try:
            pixels = self._load_image()
        except ValueError as e:
            return {"error": str(e)}

        # Step 2: Extract RGB pixels
        rgb_pixels = self._extract_all_colors(pixels)

        # Step 3: Get top N dominant colors using k-means
        try:
            dominant_colors = self._get_dominant_colors(rgb_pixels)
        except ValueError as e:
            return {"error": str(e)}

        # Step 4: Map dominant colors to HEX codes and percentages
        result = {
            "dominant": (
                {
                    "code": self._rgb_to_hex(dominant_colors[0][0]),
                    "weight": dominant_colors[0][1],
                }
                if len(dominant_colors) > 0
                else None
            ),
            "secondary": (
                {
                    "code": self._rgb_to_hex(dominant_colors[1][0]),
                    "weight": dominant_colors[1][1],
                }
                if len(dominant_colors) > 1
                else None
            ),
            "accent": (
                {
                    "code": self._rgb_to_hex(dominant_colors[2][0]),
                    "weight": dominant_colors[2][1],
                }
                if len(dominant_colors) > 2
                else None
            ),
        }

        return result
