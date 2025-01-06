from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from socials.models import CustomSocialAccount
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class CheckUserView(APIView):
    """
    소셜 회원가입 시 중복된 사용자 확인
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        existing_user = User.objects.filter(email=email).first() or User.objects.filter(phone_number=phone_number).first()

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
        decision = request.data.get('decision')  # 사용자의 선택 (link/create_new)
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        provider = request.data.get('provider')  
        social_id = request.data.get('social_id')  

        if decision == 'link':
            # 기존 계정에 소셜 계정 연동
            user = User.objects.filter(email=email).first() or User.objects.filter(phone_number=phone_number).first()
            if user:
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
            # 새 계정 생성
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
    사용자가 자신의 소셜계정 연동여부 확인인
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "is_social_connected": user.is_social_connected,
            "connected_social_providers": user.connected_social_providers,
        })

