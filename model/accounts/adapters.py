from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    # 사용자 소셜계정 연동
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        provider = sociallogin.account.provider

        if not isinstance(user.connected_social_providers, list):
            user.connected_social_providers = []
        if provider not in user.connected_social_providers:
            user.connected_social_providers.append(provider)
        
        user.is_social_connected = True
        user.save()
        return user

    def get_callback_url(self, request, socialaccount):
        return reverse('socials:kakao_callback')
        logger.debug(f"Generated callback URL: {callback_url}")
        return callback_url