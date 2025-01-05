from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', include("allauth.urls")),
    path('check-user/', views.CheckUserView.as_view(), name='check_user'),
    path('social-link-or-create/', views.SocialLinkOrCreateView.as_view(), name='social_link_or_create'),
    ]