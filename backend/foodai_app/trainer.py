import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import os
import pandas as pd

# Custom Dataset for regression labels from CSV
dataset_dir = "dataset/images"  # 이미지 경로
label_csv = "dataset/labels.csv"  # 이미지별 영양정보

class FoodDataset(Dataset):
    def __init__(self, csv_file, img_dir, transform=None):
        self.data = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.data.iloc[idx]['filename'])
        image = Image.open(img_path).convert("RGB")
        label = torch.tensor([
            self.data.iloc[idx]['calories'],
            self.data.iloc[idx]['carbs'],
            self.data.iloc[idx]['protein'],
            self.data.iloc[idx]['fat'],
        ], dtype=torch.float32)
        if self.transform:
            image = self.transform(image)
        return image, label

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

dataset = FoodDataset(label_csv, dataset_dir, transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 4)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 5
for epoch in range(epochs):
    total_loss = 0
    for images, labels in dataloader:
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")

# 모델 저장
torch.save(model.state_dict(), 'foodai_app/calorie_model.pth')
print("\n모델 학습 및 저장 완료 ✅")