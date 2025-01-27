"""
URL configuration for final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import TemplateView
from django.views.static import serve
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 수정된 버전
urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/accounts/', include("accounts.urls")),
   path('api/v1/materials/', include("materials.urls")),
   path('api/v1/socials/', include("socials.urls")),
   path('api/v1/chatbots/', include("chatbots.urls")),
   path('schema/', SpectacularAPIView.as_view(), name='schema'),
   path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   path('api/v1/platformbots/', include('platformbots.urls')),
   
   # React 라우팅을 위한 catch-all
   re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]


'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include("accounts.urls")),
    path('api/v1/materials/', include("materials.urls")),
    path('api/v1/socials/', include("socials.urls")),
    path('api/v1/chatbots/', include("chatbots.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/platformbots/', include('platformbots.urls')),
    
    # React 빌드 파일 서빙
    path('', serve, {'document_root': os.path.join(BASE_DIR, 'front_end/build'), 'path': 'index.html'}),
    re_path(r'^(?:.*)/?$', serve, {'document_root': os.path.join(BASE_DIR, 'front_end/build'), 'path': 'index.html'}),
]
'''



















'''
# 기본url.py
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include("accounts.urls")),
    path('api/v1/materials/', include("materials.urls")),
    path('api/v1/socials/', include("socials.urls")),
    path('api/v1/chatbots/', include("chatbots.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/platformbots/', include('platformbots.urls')),
    path('', TemplateView.as_view(template_name='index.html')),  # 루트 경로 추가
]
'''


'''
# 튜터님 urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
def home_view(request):
    try:
        return JsonResponse({"message": "Welcome to Final Project!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include("accounts.urls")),
    path('api/v1/materials/', include("materials.urls")),
    path('api/v1/socials/', include("socials.urls")),
    path('api/v1/chatbots/', include("chatbots.urls")),
    path('api/v1/platformbots/', include('platformbots.urls')),
    path('schema/', include('schema.urls')),
    path('', home_view, name='home'),
]
'''
