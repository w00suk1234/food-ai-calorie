from django.urls import path
from .views import PredictAPIView

urlpatterns = [
    path('api/predict/', PredictAPIView.as_view()),
]
