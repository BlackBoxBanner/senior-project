import torch
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn
import os
from .dataset import DominantColorDataset
from .model import ColorPickerCNN
from .preprocess import transform
from torchvision import transforms


def trainer(loop=10):
    # Define paths
    base_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(base_dir, "..", "train images", "Result Data.json")
    img_dir_path = os.path.join(base_dir, "..", "train images")
    model_save_path = os.path.join(
        base_dir, "..", "..", "models", "color_picker_cnn.pth"
    )

    # Data augmentation and normalization for training
    data_transforms = transforms.Compose(
        [
            transforms.RandomResizedCrop(128),
            transforms.RandomHorizontalFlip(),
            transform,  # Existing transformations
        ]
    )

    # Load dataset
    dataset = DominantColorDataset(
        json_file=json_file_path,
        img_dir=img_dir_path,
        transform=data_transforms,
    )
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

    # Initialize model, loss function, and optimizer
    model = ColorPickerCNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)  # Lower learning rate
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    # Training loop
    for epoch in range(loop):  # Number of epochs
        model.train()
        running_loss = 0.0
        for images, labels in dataloader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)

        # Step the learning rate scheduler
        scheduler.step()

        epoch_loss = running_loss / len(dataset)
        print(f"Epoch {epoch+1}/{loop}, Loss: {epoch_loss:.4f}")

    # Save the trained model
    torch.save(model.state_dict(), model_save_path)
    print("Training complete")


if __name__ == "__main__":
    trainer()
