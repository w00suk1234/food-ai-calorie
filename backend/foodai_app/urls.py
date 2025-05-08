# 📁 backend/foodai_app/urls.py (등록 필수)
from django.urls import path
from .views import PredictAPIView

urlpatterns = [
    path('api/predict/', PredictAPIView.as_view()),
]
