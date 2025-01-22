from django.urls import path
from .views.kakao_views import KakaoWebhookView

urlpatterns = [
    path('kakao/webhook/', KakaoWebhookView.as_view(), name='kakao_webhook'),
]