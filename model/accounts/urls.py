from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from. import views


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", views.SignupView.as_view(), name='signup'),
    path("preferences/", views.DashboardCompleteView.as_view(), name="preferences"),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("delete/", views.DeleteAccountView.as_view(), name='delete'),
    path('update/', views.UpdateUserView.as_view(), name='update-user'),
    path('password/change/', views.PasswordChangeView.as_view(), name='change-password'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path("profile/<str:username>/", views.SignupView.as_view(), name='profile'),
]
