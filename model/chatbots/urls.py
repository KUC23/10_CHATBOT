from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.SendArticlesToChatbotView.as_view(), name='news'),
    path('webhook/', views.KakaoChatbotView.as_view(), name='kakao-webhook'),

]