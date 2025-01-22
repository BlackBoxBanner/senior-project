import torch.nn as nn
import torch.nn.functional as F


class ColorPickerCNN(nn.Module):
    def __init__(self):
        super(ColorPickerCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, 1)
        self.conv2 = nn.Conv2d(16, 32, 3, 1)
        self.fc1 = nn.Linear(32 * 30 * 30, 128)
        self.fc2 = nn.Linear(128, 9)  # 3 colors * 3 channels (RGB)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 32 * 30 * 30)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x.view(-1, 3, 3)  # Reshape to (3 colors, 3 channels)
