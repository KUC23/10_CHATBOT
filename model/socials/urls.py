from django.urls import path
from django.urls.conf import include
from . import views
from allauth.socialaccount.providers.kakao.views import OAuth2CallbackView

# appname을 추가하면 소셜회원가입 시 오류가 생김

urlpatterns = [
    path('', include("allauth.urls")),
    path('check-user/', views.CheckUserView.as_view(), name='check_user'),
    path('social-link-or-create/', views.SocialLinkOrCreateView.as_view(), name='social_link_or_create'),
    path('link-social-account/', views.LinkSocialAccountView.as_view(), name='link_social_account'),
    path('linked-social-accounts/', views.GetLinkedSocialAccountsView.as_view(), name='linked_social_accounts'),
    path('default-social-accounts/', views.SetDefaultSocialProviderView.as_view(), name='default_social_provider'),
    ]