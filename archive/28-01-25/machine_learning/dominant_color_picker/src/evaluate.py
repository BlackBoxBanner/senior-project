import os
import torch
from .dataset import DominantColorDataset
from .model import ColorPickerCNN
from .preprocess import transform
from torch.utils.data import DataLoader
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt


def evaluate():
    # Define paths
    base_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(base_dir, "..", "evaluate images", "Result Data.json")
    img_dir_path = os.path.join(base_dir, "..", "evaluate images")
    model_path = os.path.join(
        base_dir, "..", "..", "models", "color_picker_cnn.pth"
    )

    # Load dataset
    dataset = DominantColorDataset(
        json_file=json_file_path,
        img_dir=img_dir_path,
        transform=transform,
    )
    dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=4)

    # Load model
    model = ColorPickerCNN()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()

    all_labels = []
    all_outputs = []

    with torch.no_grad():
        for images, labels in dataloader:
            outputs = model(images)
            all_labels.append(labels)
            all_outputs.append(outputs)

    all_labels = torch.cat(all_labels).view(-1, 9)  # Reshape to (num_samples, 9)
    all_outputs = torch.cat(all_outputs).view(-1, 9)  # Reshape to (num_samples, 9)

    labels_np = all_labels.numpy()
    outputs_np = all_outputs.numpy()

    mse = mean_squared_error(labels_np, outputs_np)
    mae = mean_absolute_error(labels_np, outputs_np)
    r2 = r2_score(labels_np, outputs_np)

    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")
    print(f"R-squared: {r2}")

    # Visualize some predictions
    visualize_predictions(labels_np, outputs_np)


def visualize_predictions(labels, outputs, num_samples=5):
    fig, axes = plt.subplots(num_samples, 2, figsize=(10, num_samples * 2))
    for i in range(num_samples):
        axes[i, 0].imshow(labels[i].reshape(3, 3, 1), cmap="viridis")
        axes[i, 0].set_title("Actual")
        axes[i, 0].axis("off")
        axes[i, 1].imshow(outputs[i].reshape(3, 3, 1), cmap="viridis")
        axes[i, 1].set_title("Predicted")
        axes[i, 1].axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    evaluate()
