from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .ai_model import analyze_food_image

class PredictAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.data.get('image')
        if not image:
            return Response({"error": "No image provided."}, status=400)
        result = analyze_food_image(image)
        return Response(result)