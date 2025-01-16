from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from socials.models import CustomSocialAccount
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import JsonResponse
from .serialilzers import SocialAccountSerializer
from django.db import IntegrityError

def find_existing_user(email=None, phone_number=None):
    if email:
        return User.objects.filter(email=email).first()
    if phone_number:
        return User.objects.filter(phone_number=phone_number).first()
    return None


# 중복된 이메일, 핸드폰번호 확인
class CheckUserView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')

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

# 중복된 계정일 때 연동 또는 새로운 계정 생성
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


# 로그인한 사용자가 소셜계정을 연동하고 싶을 때
class LinkSocialAccountView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')
        user = request.user

        if CustomSocialAccount.objects.filter(provider=provider, uid=social_id).exists():
            return Response({
                "status": "error",
                "message": "이미 연결된 소셜 계정입니다.",
                "redirect_url": None
                }, status=400)

        CustomSocialAccount.objects.create(user=user, provider=provider, uid=social_id)
        if provider not in user.connected_social_providers:
            user.connected_social_providers.append(provider)
        user.is_social_connected = True
        user.save()

        return Response({
            "message": f"{provider} 계정이 성공적으로 연결되었습니다.", 
            "redirect_url": f"/profile/{user.username}/"
            })


# 소셜계정 연동여부 확인 /안쓰는 뷰이면 삭제 가능
class GetLinkedSocialAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "is_social_connected": user.is_social_connected,
            "connected_social_providers": user.connected_social_providers,
        })

# 소셜계정이 두 개 이상일 때, 정보를 받을 기본 소셜계정 선택
class SetDefaultSocialProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider = request.data.get('provider')

        if provider not in request.user.connected_social_providers:
            return Response({
                "status": "error",
                "message": "연결되지 않은 소셜 계정입니다.",
                "redirect_url": None
            }, status=400)
        
        user=request.user
        user.default_social_provider = provider
        user.save()

        return Response({
            "status": "success",
            "message": f"{provider} 계정이 기본 소셜 계정으로 설정되었습니다.",
            "redirect_url": f"/profile/{user.username}/"
        })
