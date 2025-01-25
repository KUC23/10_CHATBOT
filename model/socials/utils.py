from allauth.socialaccount.models import SocialToken
import requests
from allauth.socialaccount.models import SocialToken, SocialApp

def get_access_token(user, provider):
    try:
        token = SocialToken.objects.get(account__user=user, account__provider=provider)
        return token.token
    except SocialToken.DoesNotExist:
        return None  
    


def refresh_access_token(user, provider):
    try:
        app = SocialApp.objects.get(provider=provider)  
        token = SocialToken.objects.get(account__user=user, account__provider=provider) 

        if provider == "kakao":
            url = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type": "refresh_token",
                "client_id": app.client_id,
                "refresh_token": token.token_secret,  
            }
        elif provider == "discord":
            url = "https://discord.com/api/oauth2/token"
            data = {
                "grant_type": "refresh_token",
                "client_id": app.client_id,
                "client_secret": app.secret,
                "refresh_token": token.token_secret, 
            }
        else:
            raise Exception(f"지원하지 않는 provider입니다: {provider}")

        response = requests.post(url, data=data)
        response_data = response.json()

        if "access_token" in response_data:
            token.token = response_data["access_token"]
            token.save()

            if "refresh_token" in response_data:
                token.token_secret = response_data["refresh_token"]
                token.save()

            return token.token 

        raise Exception(response_data.get("error_description", "Failed to refresh token"))
    except SocialApp.DoesNotExist:
        raise Exception(f"{provider} 소셜 앱 설정이 없습니다.")
    except SocialToken.DoesNotExist:
        raise Exception(f"{provider} 소셜 토큰이 없습니다.")

