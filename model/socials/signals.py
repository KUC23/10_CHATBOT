from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from accounts.models import User  

# @receiver(user_signed_up)
# def disable_password_for_social_user(sender, request, user, **kwargs):
#     user.set_unusable_password()
#     user.save()

@receiver(user_signed_up)
def set_test_password(sender, request, user, **kwargs):
    user.set_password("test1234")  
    user.save()