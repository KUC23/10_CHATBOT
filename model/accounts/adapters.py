from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


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


