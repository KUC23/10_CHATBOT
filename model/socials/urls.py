from django.urls import path
from django.urls.conf import include
from . import views
from allauth.socialaccount.providers.kakao.views import OAuth2CallbackView

app_name = "socials"

urlpatterns = [
    path('', include("allauth.urls")),
    path('check-user/', views.CheckUserView.as_view(), name='check_user'),
    path('social-link-or-create/', views.SocialLinkOrCreateView.as_view(), name='social_link_or_create'),
    path('link-social-account/', views.LinkSocialAccountView.as_view(), name='link_social_account'),
    path('linked-social-accounts/', views.GetLinkedSocialAccountsView.as_view(), name='linked_social_accounts'),
    ]