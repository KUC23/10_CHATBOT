from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from. import views

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", views.SignupView.as_view(), name='signup'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("delete/", views.DeleteAccountView.as_view(), name='delete'),
    path('update/', views.UpdateUserView.as_view(), name='update-user'),
    path("<str:username>/", views.SignupView.as_view(), name='view-info'),
]
