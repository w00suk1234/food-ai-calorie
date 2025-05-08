import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from sklearn.preprocessing import LabelEncoder
from PIL import Image
import os
import pandas as pd

# 데이터셋 경로
image_dir = "dataset/images"
label_path = "dataset/labels.csv"

# 라벨 인코딩
df = pd.read_csv(label_path)
le = LabelEncoder()
df["food_label"] = le.fit_transform(df["food"])
print("클래스 목록:", le.classes_)

class FoodDataset(Dataset):
    def __init__(self, dataframe, image_dir, transform=None):
        self.df = dataframe
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(self.image_dir, row['filename'])
        image = Image.open(img_path).convert("RGB")
        food_label = torch.tensor(row['food_label'], dtype=torch.long)
        nutrition = torch.tensor([
            row['calories'], row['carbs'], row['protein'], row['fat']
        ], dtype=torch.float32)

        norm_factors = torch.tensor([2000.0, 600.0, 200.0, 100.0])
        nutrition = nutrition / norm_factors

        if self.transform:
            image = self.transform(image)

        return image, food_label, nutrition

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

dataset = FoodDataset(df, image_dir, transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# 모델 정의
class FoodNet(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        base = models.resnet18(pretrained=True)
        self.backbone = nn.Sequential(*list(base.children())[:-1])
        in_features = base.fc.in_features
        self.class_head = nn.Linear(in_features, num_classes)
        self.reg_head = nn.Sequential(
            nn.Linear(in_features, 4),
            nn.Softplus()
)


    def forward(self, x):
        x = self.backbone(x).squeeze()
        return self.class_head(x), self.reg_head(x)

model = FoodNet(num_classes=len(le.classes_))
criterion_class = nn.CrossEntropyLoss()
criterion_reg = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 10
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch_idx, (images, labels_class, labels_reg) in enumerate(dataloader):
        pred_class, pred_reg = model(images)
        loss_class = criterion_class(pred_class, labels_class)
        loss_reg = criterion_reg(pred_reg, labels_reg)
        loss = loss_class * 2.0 + loss_reg * 0.1

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

        if epoch == 0 and batch_idx == 0:
            print("[예측된 클래스]:", torch.argmax(pred_class, dim=1).tolist())

    print(f"Epoch {epoch+1}/{epochs}, Class Loss: {loss_class.item():.4f}, Reg Loss: {loss_reg.item():.4f}, Total Loss: {total_loss:.4f}")

# 모델 저장
torch.save({
    "model_state_dict": model.state_dict(),
    "label_encoder": le.classes_.tolist()
}, "foodai_app/calorie_model.pth")

print("\n 모델 학습 및 저장 완료!")
