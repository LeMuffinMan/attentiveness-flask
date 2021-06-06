from PIL import Image, ImageOps
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import time
import pandas as pd
# import json
from IPython.display import clear_output
torch.set_printoptions(linewidth=120)
torch.set_grad_enabled(True)



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class Network(nn.Module):
	def __init__(self):
		super().__init__()
		self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5)
		self.conv2 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size=5)

		self.fc1 = nn.Linear(in_features=12*9*9, out_features=120)
		self.fc2 = nn.Linear(in_features=120, out_features=60)
		self.out = nn.Linear(in_features=60, out_features=7)

	def forward(self, t):
		t = self.conv1(t)
		t = F.relu(t)
		t = F.max_pool2d(t, kernel_size=2, stride=2)

		t = self.conv2(t)
		t = F.relu(t)
		t = F.max_pool2d(t, kernel_size=2, stride=2)

		t = t.reshape(-1, 12*9*9)

		t = self.fc1(t)
		t = F.relu(t)

		t = self.fc2(t)
		t = F.relu(t)

		t = self.out(t)

		return t


class webopencv(object):
	def __init__(self):
		pass

	def process(self):
		model = torch.load("modelResults.pt")
		torch.save(model.state_dict(), "model_state_dict.pt")


w = webopencv()
w.process()


