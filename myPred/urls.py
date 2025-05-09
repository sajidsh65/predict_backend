# myPred/urls.py
from django.urls import path
from .views import predict_mbti, get_mbti_qualities, get_qualities

urlpatterns = [
    path('predict/', predict_mbti, name='predict_mbti'),
    path('qualities/', get_mbti_qualities, name='qualities'),
    path('qualities/<str:mbti_type>/', get_qualities, name='get-qualities'),
    
]