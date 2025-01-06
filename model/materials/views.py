from django.shortcuts import render

# Create your views here.

#정보전송로직에서 소셜계정선택
# default_provider = user.default_social_provider
# if not default_provider:
#     # 기본 제공 계정이 설정되지 않았다면 첫 번째 연결된 계정을 사용하도록록
#     default_provider = user.connected_social_providers[0]