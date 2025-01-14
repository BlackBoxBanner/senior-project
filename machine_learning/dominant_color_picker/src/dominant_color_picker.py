import torch
from PIL import Image
from .model import ColorPickerCNN
from .preprocess import transform
import os


def _load_model(model_path):
    model = ColorPickerCNN()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model


def validate_rgb_values(rgb_values):
    """Ensure RGB values are within the valid range [0, 255]."""
    return tuple(
        tuple(max(0, min(255, int(channel))) for channel in color)
        for color in rgb_values
    )


def predict_dominant_colors(image_path):
    model_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "models", "color_picker_cnn.pth"
    )
    model = _load_model(model_path)
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        output = model(image)

    print(output)

    # Convert output to RGB values
    dominant_colors = output.squeeze(0).numpy() * 255
    dominant_colors = dominant_colors.astype(int)

    # Validate RGB values
    rgb_values = validate_rgb_values(dominant_colors)

    return rgb_values
