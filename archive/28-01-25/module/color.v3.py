from collections import Counter
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import cv2

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
        Convert an RGB tuple to a HEX string.
        :param rgb: Tuple (R, G, B).
        :return: HEX string.
        """
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def extract_dominant_colors(self):
        """
        Extract dominant colors from an image using a histogram-based approach.
        
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
        
        # Compute the histogram for each color channel (bins = 16 for better grouping)
        hist, edges = np.histogramdd(pixels, bins=(16, 16, 16))
        
        # Flatten the histogram and get the top bins
        hist_flat = hist.flatten()
        top_indices = np.argsort(hist_flat)[-self.num_colors:][::-1]  # Top `num_colors`
        
        # Calculate the RGB values of the top bins
        bin_size = 256 / 16  # Each bin covers a range of 256/16 = 16 values
        dominant_colors = []
        total_pixels = np.sum(hist_flat)  # Total number of pixels in the image
        
        for index in top_indices:
            r_bin = index // (16 * 16)
            g_bin = (index // 16) % 16
            b_bin = index % 16
            
            # Calculate the RGB values of the bin center
            r = int((r_bin + 0.5) * bin_size)
            g = int((g_bin + 0.5) * bin_size)
            b = int((b_bin + 0.5) * bin_size)
            
            # Calculate the percentage of pixels in this bin
            percentage = (hist_flat[index] / total_pixels) * 100
            
            dominant_colors.append({
                "color": (r, g, b),
                "percentage": percentage
            })
        
        return dominant_colors