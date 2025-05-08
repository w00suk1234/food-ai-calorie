from django.contrib import admin
from django.urls import path
from foodai_backend.views import PredictView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/predict/', PredictView.as_view()),
]
