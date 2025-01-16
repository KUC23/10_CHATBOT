from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import resolve_url

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        provider = sociallogin.account.provider

        # 소셜 계정 연결 상태 설정
        if provider not in user.connected_social_providers:
            user.connected_social_providers.append(provider)
            user.is_social_connected = True

        # 기본 소셜 제공자 설정
        if not user.default_social_provider:
            user.default_social_provider = provider

        user.save()
        return user


    # 회원가입 및 로그인 후 redirect
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated and user.is_social_connected and user.is_first_login:
            user.is_first_login = False  
            user.save()
            return resolve_url("/preferences/")
        return resolve_url("/")  

