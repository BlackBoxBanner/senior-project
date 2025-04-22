import io
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


class ColorModule:
    def __init__(self, image_byte: bytes, num_colors: int = 3):
        """
        Initialize the ColorModule with the image bytes and the number of dominant colors to extract.
        :param image_byte: Bytes of the image file.
        :param num_colors: Number of dominant colors to extract (default is 3).
        """
        if not isinstance(image_byte, (bytes, bytearray)):
            raise TypeError("image_byte must be a bytes-like object")
        self.image_byte = image_byte
        self.num_colors = num_colors
        self.image = self._load_image()

    def _load_image(self):
        """
        Load the image from bytes and convert to RGB.
        :return: A numpy array of the image's RGB pixels.
        """
        image = Image.open(io.BytesIO(self.image_byte)).convert("RGB")
        return np.array(image)

    def _remove_background(self, image):
        """
        Remove the background color from the image.
        :param image: A numpy array of the image's RGB pixels.
        :return: A numpy array of the image's RGB pixels without the background.
        """
        # Convert image to grayscale and apply threshold to create a mask
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Apply the mask to the image
        image_no_bg = cv2.bitwise_and(image, image, mask=mask)
        return image_no_bg

    def extract_dominant_colors(self):
        """
        Extract the dominant colors from the image.
        :return: A list of the dominant colors in the image.
        """
        # Convert image bytes to a numpy array
        image = self.image

        # Remove the background from the image
        image_no_bg = self._remove_background(image)

        # Reshape the image to be a list of pixels
        pixels = image_no_bg.reshape(-1, 3)

        # Remove any fully transparent pixels
        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

        # Use KMeans to find the dominant colors
        kmeans = KMeans(n_clusters=self.num_colors)
        kmeans.fit(pixels)

        # Get the RGB values of the cluster centers and their counts
        colors, counts = np.unique(kmeans.labels_, return_counts=True)
        dominant_colors = [
            (kmeans.cluster_centers_[i].astype(int).tolist(), counts[i])
            for i in range(len(colors))
        ]
        return dominant_colors
