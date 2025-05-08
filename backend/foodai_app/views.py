from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .ai_model import analyze_food_image

print(" [DEBUG] views.py 실행됨")

class PredictAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.data:
            return Response({"error": "이미지 파일이 필요합니다."}, status=400)

        image = request.data['image']
        result = analyze_food_image(image)
        return Response(result)
