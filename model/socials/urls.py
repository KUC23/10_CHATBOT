from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('', include("allauth.urls")),
    path('check-user/', views.CheckUserView.as_view(), name='check_user'),
    path('social-link-or-create/', views.SocialLinkOrCreateView.as_view(), name='social_link_or_create'),
    path('link-social-account/', views.LinkSocialAccountView.as_view(), name='link_social_account'),
    path('linked-social-accounts/', views.GetLinkedSocialAccountsView.as_view(), name='linked_social_accounts'),
    path('default-social-accounts/', views.SetDefaultSocialProviderView.as_view(), name='default_social_provider'),
    path('delete-social-account/', views.DeleteSocialAccountView.as_view(), name='delete_social_account'),
    path("access-token/", views.SocialAccessTokenView.as_view(), name="social_access_token"),
]