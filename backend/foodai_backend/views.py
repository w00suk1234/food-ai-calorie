from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

class PredictView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        if not image:
            return Response({'error': 'No image provided.'}, status=400)

        result = {
            'food': '샐러드',
            'calories': 210,
            'carbs': 15,
            'protein': 8,
            'fat': 12,
            'is_diet': True,
            'message': '이 음식은 다이어트 식단에 적합해요!'
        }
        return Response(result)
