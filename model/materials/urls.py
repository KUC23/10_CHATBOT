from django.urls import path
from . import views

app_name = "materials"

urlpatterns = [
    path('news/', views.NewsView.as_view(), name='news'),
    ]