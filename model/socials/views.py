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


class CheckUserView(APIView):
    """
    소셜 회원가입 시 중복된 사용자 확인
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')

        # Check if user already exists
        existing_user = find_existing_user(email=email, phone_number=phone_number)
        existing_social = CustomSocialAccount.objects.filter(provider=provider, uid=social_id).exists()

        if existing_social:
            return Response({
                "status": "exists",
                "message": f"이미 {provider} 계정이 연동된 상태입니다."
            })

        if existing_user:
            return Response({
                "status": "exists",
                "message": "중복된 계정이 존재합니다.",
                "options": {
                    "link_account": True,
                    "create_new_account": True
                }
            })

        return Response({
            "status": "not_exists",
            "message": "새 계정을 생성할 수 있습니다."
        })


class SocialLinkOrCreateView(APIView):
    """
    소셜회원 가입 중복된 사용자 정보일 때, 기존 계정 연동 또는 새 계정 생성 처리
    """

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
                        "message": "이미 연결된 소셜 계정입니다."
                    }, status=400)

                CustomSocialAccount.objects.create(
                    user=user,
                    provider=provider,
                    uid=social_id
                )
                return Response({
                    "status": "success",
                    "message": "기존 계정에 소셜 계정이 연동되었습니다."
                })

            return Response({
                "status": "error",
                "message": "연동할 계정을 찾을 수 없습니다."
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
                    "message": "새 계정이 생성되었습니다."
                })
            except IntegrityError:
                return Response({
                    "status": "error",
                    "message": "계정 생성 중 문제가 발생했습니다. 입력 정보를 확인해주세요."
                }, status=400)

        return Response({
            "status": "error",
            "message": "잘못된 요청입니다."
        }, status=400)


class LinkSocialAccountView(APIView):
    """
    로그인한 사용자가 소셜계정을 연동할 때
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')
        user = request.user

        if CustomSocialAccount.objects.filter(user=user, provider=provider).exists():
            return Response({"message": "이미 연결된 소셜 계정입니다."}, status=400)

        CustomSocialAccount.objects.create(user=user, provider=provider, uid=social_id)
        if provider not in user.connected_social_providers:
            user.connected_social_providers.append(provider)
        user.is_social_connected = True
        user.save()

        return Response({"message": f"{provider} 계정이 성공적으로 연결되었습니다."})


class GetLinkedSocialAccountsView(APIView):
    """
    사용자가 자신의 소셜계정 연동여부 확인
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "is_social_connected": user.is_social_connected,
            "connected_social_providers": user.connected_social_providers,
        })


class SetDefaultSocialProviderView(APIView):
    """
    사용자가 정보를 받을 기본 소셜 계정을 선택
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        provider = request.data.get('provider')

        if provider not in request.user.connected_social_providers:
            return Response({
                "status": "error",
                "message": "연결되지 않은 소셜 계정입니다."
            }, status=400)

        request.user.default_social_provider = provider
        request.user.save()

        return Response({
            "status": "success",
            "message": f"{provider} 계정이 기본 소셜 계정으로 설정되었습니다."
        })
