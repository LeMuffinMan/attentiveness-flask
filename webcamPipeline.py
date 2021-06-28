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
import json
from IPython.display import clear_output

torch.set_printoptions(linewidth=120)
torch.set_grad_enabled(True)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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

cap = cv2.VideoCapture(0)
while True:
	_, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)

	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

		grayFrameCropped = gray[y:y+h, x:x+w]
		dim = (48,48)
		grayFrameCroppedResized = cv2.resize(grayFrameCropped, dim, interpolation = cv2.INTER_AREA)
		grayFrameCroppedResizedTensor = torch.from_numpy(grayFrameCroppedResized)
		grayFrameCroppedResizedTensorChannel = grayFrameCroppedResizedTensor.unsqueeze(dim=0).type(torch.FloatTensor)
		grayFrameCroppedResizedTensorChannelDim = grayFrameCroppedResizedTensorChannel.unsqueeze(dim=0).type(torch.FloatTensor)
		#  I am not sorry for naming this variable "grayFrameCroppedResizedTensorChannelDim"
		model = torch.load('modelResults.pt')
		result = model(grayFrameCroppedResizedTensorChannelDim)
		m = nn.Softmax()
		predictions = m(result)
		prediction = torch.argmax(predictions).item()

		confidence = torch.max(predictions)

		classList = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
		classification = classList[prediction]
		cv2.putText(img, classification, (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.9, (36,255,12), 2)

	cv2.imshow('img', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()

