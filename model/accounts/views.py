from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, DeleteAccountSerializer, UpdateUserSerializer, PasswordChangeSerializer
from .models import User, Category
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_phone = request.data.get('username')  
        password = request.data.get('password')

        user = authenticate(request, username=username_or_phone, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"detail": "비밀번호 또는 사용자 이름이 잘못되었습니다."},
                        status=status.HTTP_401_UNAUTHORIZED)

class SignupView(APIView):
    def get(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            serializer = RegisterUserSerializer(request.user)
            return Response(serializer.data)
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            default_category, _ = Category.objects.get_or_create(name="Main")
            user.categories.add(default_category)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "회원가입이 완료되었습니다.",
                "redirect_url": "/preferences/",
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )

        
class DashboardCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        messenger_platform = request.data.get("messenger_platform")
        category_ids = request.data.get("categories", [])

        if messenger_platform:
            user.default_social_provider = messenger_platform
        
        if category_ids:
            valid_categories = Category.objects.filter(id__in=category_ids)
            if not valid_categories.exists():
                return Response({"error": "유효하지 않은 카테고리 ID입니다."}, status=status.HTTP_400_BAD_REQUEST)
            user.categories.set(valid_categories)

        user.save()
        return Response(
            {"message": "회원가입 완료", "redirect_url": f"/profile/{user.username}/"},
            status=status.HTTP_200_OK
        )
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"] 
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.delete()
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)


class UpdateUserView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "수정 완료", "redirect_url": f"/profile/{user.username}/"}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        categories = Category.objects.all().values("id", "name")
        return Response(list(categories))
