import torch
import torch.nn as nn

class CNN_IDS(nn.Module):
    """
    基于CNN的异常检测模型
    """
    def __init__(self):
        super(CNN_IDS, self).__init__()
        self.cnn1 = torch.nn.Conv2d(1, 32, kernel_size=15, stride=1, padding=2) # 60 * 60 --> 50 * 50
        self.pool1 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 50 * 50 --> 25 * 25
        self.cnn2 = torch.nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2) # 25 * 25 --> 25 * 25
        self.pool2 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 25 * 25 --> 13 * 13
        self.cnn3 = torch.nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=2) # 13 * 13 --> 13 * 13
        self.pool3 = torch.nn.MaxPool2d(kernel_size=2, stride=2) # 13 * 13 --> 7 * 7
        self.fc = torch.nn.Linear(6*6*64, 1)
        self.active = nn.Sigmoid()

    def forward(self, x):
        x = self.cnn1(x)
        x = self.pool1(x)
        x = self.cnn2(x)
        x = self.pool2(x)
        x = self.cnn3(x)
        x = self.pool3(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc(x)
        x = self.active(x)
        return x

