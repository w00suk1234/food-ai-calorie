# 📁 backend/foodai_app/ai_model.py
import torch
from torchvision import transforms, models
from PIL import Image

# 모델 구조 정의
def load_model():
    model = models.resnet18()
    model.fc = torch.nn.Linear(model.fc.in_features, 4)
    model.load_state_dict(torch.load('foodai_app/calorie_model.pth', map_location='cpu'))
    model.eval()
    return model

model = load_model()

def analyze_food_image(image_file):
    image = Image.open(image_file).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor).squeeze().tolist()

    return {
        "food": "예측된 음식",
        "calories": round(output[0], 1),
        "carbs": round(output[1], 1),
        "protein": round(output[2], 1),
        "fat": round(output[3], 1),
        "message": calorie_message(output[0])
    }

def calorie_message(cal):
    if cal < 300:
        return "다이어트에 매우 적합한 식단입니다."
    elif cal < 500:
        return "가벼운 식사로 적당합니다."
    else:
        return "고칼로리 주의! 식사량을 조절하세요."
