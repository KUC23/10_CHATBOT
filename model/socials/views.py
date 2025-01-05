from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from socials.models import SocialAccount  


class CheckUserView(APIView):
    """
    소셜 로그인 데이터를 기반으로 중복된 사용자 정보 확인
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
    사용자의 선택에 따라 기존 계정 연동 또는 새 계정 생성 처리
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
                SocialAccount.objects.create(
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
            SocialAccount.objects.create(
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
