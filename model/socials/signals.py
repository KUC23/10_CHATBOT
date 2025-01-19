from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from accounts.models import User  

# 배포용: 소셜 로그인 사용자 비밀번호 비활성화
# 개발환경에서 아래 함수 주석처리
@receiver(user_signed_up)
def disable_password_for_social_user(sender, request, user, **kwargs):
    user.set_unusable_password()
    user.save()



# # 개발용: 테스트 환경에서 소셜 사용자에게 기본 비밀번호 설정
# # 배포환경에서 아래 함수 주석처리
# @receiver(user_signed_up)
# def set_test_password(sender, request, user, **kwargs):
#     user.set_password("test1234")  
#     user.save()

