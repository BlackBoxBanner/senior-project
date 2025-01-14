import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


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

    def extract_dominant_colors(self):
        """
        Extract dominant colors from an image using KMeans clustering.

        Returns:
            dominant_colors (list): List of dominant colors (RGB tuples) with percentages.
        """
        # Load the image and convert to RGB
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize the image to reduce noise and processing time
        resized_image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)

        # Flatten the image into an array of pixels
        pixels = resized_image.reshape(-1, 3)

        # Use KMeans to cluster the pixel colors
        kmeans = KMeans(n_clusters=self.num_colors)
        kmeans.fit(pixels)

        # Get the cluster centers (dominant colors)
        dominant_colors = kmeans.cluster_centers_.astype(int)

        # Get the percentage of each color
        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        percentages = counts / counts.sum() * 100

        # Combine the colors and percentages
        dominant_colors_with_percentages = [
            {"color": tuple(color), "percentage": percentage}
            for color, percentage in zip(dominant_colors, percentages)
        ]

        return dominant_colors_with_percentages
