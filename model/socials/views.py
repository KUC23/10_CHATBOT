from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from socials.models import CustomSocialAccount
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import JsonResponse
from .serialilzers import SocialAccountSerializer
from django.db import IntegrityError
from .utils import get_access_token, refresh_access_token

def find_existing_user(email=None, phone_number=None):
    if email:
        return User.objects.filter(email=email).first()
    if phone_number:
        return User.objects.filter(phone_number=phone_number).first()
    return None


class CheckUserView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        phone_number = request.data.get('phone_number', '').strip()
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')

        if not email and not phone_number:
            return Response({
                "status": "error",
                "message": "이메일 또는 휴대폰 번호를 입력해야 합니다.",
                "redirect_url": None
            }, status=400)

        existing_user = find_existing_user(email=email, phone_number=phone_number)
        existing_social = CustomSocialAccount.objects.filter(provider=provider, uid=social_id).exists()

        if existing_social:
            return Response({
                "status": "exists",
                "message": f"이미 {provider} 계정이 연동된 상태입니다.",
                "redirect_url": "/preferences/"
            })

        if existing_user:
            return Response({
                "status": "exists",
                "message": "중복된 계정이 존재합니다.",
                "options": {
                    "link_account": True,
                    "create_new_account": True
                },
                "redirect_url": "/social-link-or-create/"
            })

        return Response({
            "status": "not_exists",
            "message": "새 계정을 생성할 수 있습니다.",
            "redirect_url": "/preferences/"
        })

class SocialLinkOrCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SocialAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        decision = serializer.validated_data['decision']
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        provider = serializer.validated_data['provider']
        social_id = serializer.validated_data['social_id']

        if decision == 'link':
            user = find_existing_user(email=email, phone_number=phone_number)
            if user:
                if CustomSocialAccount.objects.filter(user=user, provider=provider).exists():
                    return Response({
                        "status": "error",
                        "message": "이미 연결된 소셜 계정입니다.",
                        "redirect_url": None
                    }, status=400)

                CustomSocialAccount.objects.create(
                    user=user,
                    provider=provider,
                    uid=social_id
                )
                return Response({
                    "status": "success",
                    "message": "기존 계정에 소셜 계정이 연동되었습니다.",
                    "redirect_url": "/"
                })

            return Response({
                "status": "error",
                "message": "연동할 계정을 찾을 수 없습니다.",
                "redirect_url": None
            }, status=400)

        elif decision == 'create_new':
            try:
                new_user = User.objects.create(
                    username=f"{provider}_{social_id}",
                    email=email,
                    phone_number=phone_number
                )
                CustomSocialAccount.objects.create(
                    user=new_user,
                    provider=provider,
                    uid=social_id
                )
                return Response({
                    "status": "success",
                    "message": "새 계정이 생성되었습니다.",
                    "redirect_url": "/preferences/"
                })
            except IntegrityError:
                return Response({
                    "status": "error",
                    "message": "계정 생성 중 문제가 발생했습니다. 입력 정보를 확인해주세요.",
                    "redirect_url": None
                }, status=400)

        return Response({
            "status": "error",
            "message": "잘못된 요청입니다.",
            "redirect_url": None
        }, status=400)


class LinkSocialAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')
        user = request.user

        existing_account = CustomSocialAccount.objects.filter(provider=provider, uid=social_id, user=user).exists()
        if existing_account:
            return Response({
                "status": "success",
                "message": f"이미 {provider} 계정이 연동되어 있습니다.",
                "redirect_url": f"/profile/{user.username}/"
            })

        if provider == user.default_social_provider:
            return Response({
                "status": "success",
                "message": f"{provider} 계정은 이미 기본 제공자로 설정되어 있습니다.",
                "redirect_url": f"/profile/{user.username}/"
            })

        CustomSocialAccount.objects.create(user=user, provider=provider, uid=social_id)
        if provider not in user.connected_social_providers:
            user.connected_social_providers.append(provider)

        user.is_social_connected = True
        user.save()

        return Response({
            "status": "success",
            "message": f"{provider} 계정이 성공적으로 연동되었습니다.",
            "redirect_url": f"/profile/{user.username}/"
        })


class GetLinkedSocialAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "is_social_connected": user.is_social_connected,
            "connected_social_providers": user.connected_social_providers,
        })

class SetDefaultSocialProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider = request.data.get('provider')
        user = request.user

        if provider not in user.connected_social_providers:
            return Response({
                "status": "error",
                "message": f"{provider} 계정이 연결되지 않았습니다. 먼저 연동하세요.",
                "redirect_url": "/link-social-account/"
            }, status=400)

        user.default_social_provider = provider
        user.save()

        return Response({
            "status": "success",
            "message": f"{provider} 계정이 기본 소셜 계정으로 설정되었습니다.",
            "redirect_url": f"/profile/{user.username}/"
        })

class DeleteSocialAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        provider = request.data.get('provider')  
        user = request.user

        account_to_delete = CustomSocialAccount.objects.filter(user=user, provider=provider).first()
        if not account_to_delete:
            return Response({
                "status": "error",
                "message": f"{provider} 계정이 연결되어 있지 않습니다."
            }, status=404)

        if len(user.connected_social_providers) == 1:
            return Response({
                "status": "error",
                "message": "적어도 하나의 소셜 계정은 유지되어야 합니다. 다른 계정을 추가한 후 시도하세요.",
                "redirect_url": "/link-social-account/"
            }, status=400)


        account_to_delete.delete()

        if provider in user.connected_social_providers:
            user.connected_social_providers.remove(provider)

        if user.default_social_provider == provider:
            user.default_social_provider = user.connected_social_providers[0]  

        user.save()

        return Response({
            "status": "success",
            "message": f"{provider} 계정이 성공적으로 삭제되었습니다."
        }, status=200)

class SocialAccessTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        provider = request.query_params.get("provider") 
        if not provider:
            return Response({"error": "provider를 지정해주세요 (예: kakao, discord)"}, status=400)

        user = request.user

        access_token = get_access_token(user, provider)

        if not access_token:
            return Response({"error": f"{provider} 계정의 Access Token이 없습니다."}, status=404)

        return Response({"access_token": access_token})

    def post(self, request, *args, **kwargs):
        provider = request.data.get("provider")  
        if not provider:
            return Response({"error": "provider를 지정해주세요 (예: kakao, discord)"}, status=400)

        user = request.user

        try:
            new_access_token = refresh_access_token(user, provider)
            return Response({"access_token": new_access_token})
        except Exception as e:
            return Response({"error": str(e)}, status=400)