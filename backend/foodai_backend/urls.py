from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('foodai_app.urls')),  #  이 줄이 반드시 있어야 함
]
