import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn


# FoodNet 모델 정의 (분류 + 회귀)
class FoodNet(torch.nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        base = models.resnet18(pretrained=False)
        self.backbone = torch.nn.Sequential(*list(base.children())[:-1])
        in_features = base.fc.in_features
        self.class_head = torch.nn.Linear(in_features, num_classes)
        self.reg_head = nn.Sequential(
              nn.Linear(in_features, 4),
              nn.Softplus()
)


    def forward(self, x):
        x = self.backbone(x).squeeze()
        class_out = self.class_head(x)
        reg_out = self.reg_head(x)
        return class_out, reg_out

# 모델 로드
checkpoint = torch.load("foodai_app/calorie_model.pth", map_location='cpu')
class_names = checkpoint["label_encoder"]
model = FoodNet(num_classes=len(class_names))
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# 영어 → 한글 라벨 매핑
to_korean = {
    "hamburger": "햄버거",
    "pizza": "피자",
    "salad": "샐러드",
    "bibimbap": "비빔밥",
    "ramen": "라면",
}

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 칼로리 해석 메시지
def calorie_message(cal):
    if cal < 300:
        return "다이어트에 적합한 식단입니다."
    elif cal < 500:
        return "가벼운 식사로 적당합니다."
    else:
        return "고칼로리 음식입니다. 섭취에 주의하세요."

# 분석 함수
def analyze_food_image(image_file):
    image = Image.open(image_file).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        class_logits, nutrition = model(input_tensor)
        pred_class_idx = torch.argmax(class_logits, dim=0).item()
        eng_name = class_names[pred_class_idx]
        food_name = to_korean.get(eng_name, eng_name)
        nutrition = nutrition.squeeze().tolist()

        # 정규화 복원
        norm_factors = [2000.0, 600.0, 200.0, 100.0]
        nutrition = [n * f for n, f in zip(nutrition, norm_factors)]

    return {
        "food": food_name,
        "calories": round(nutrition[0], 1),
        "carbs": round(nutrition[1], 1),
        "protein": round(nutrition[2], 1),
        "fat": round(nutrition[3], 1),
        "message": calorie_message(nutrition[0])
    }
