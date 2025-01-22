from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import resolve_url

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        provider = sociallogin.account.provider

        if provider not in user.connected_social_providers:
            user.connected_social_providers.append(provider)
            user.is_social_connected = True

        if not user.default_social_provider:
            user.default_social_provider = provider

        user.save()
        return user


    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated and user.is_social_connected and user.is_first_login:
            user.is_first_login = False  
            user.save()
            return resolve_url("/preferences/")
        return resolve_url("/")  

