from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from. import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", views.SignupView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("delete/", views.DeleteAccountView.as_view()),
    path("<str:username>/", views.SignupView.as_view()),
]
