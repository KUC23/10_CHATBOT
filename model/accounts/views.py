from django.shortcuts import get_object_or_404
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
        if request.user.is_authenticated:
            user=get_object_or_404(User, username=username)
            serializer=RegisterUserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    # def post(self, request):
    #     if not request.user.is_authenticated:
    #         return Response({"message": "로그인이 필요합니다."}, status=401)
        
    #     category_ids = request.data.get("categories", [])
    #     if not isinstance(category_ids, list) or not category_ids:
    #         return Response({"message": "관심사를 선택해주세요."}, status=400)

    #     try:
    #         categories = Category.objects.filter(id__in=category_ids)
    #         if not categories.exists():
    #             return Response({"message": "유효하지 않은 카테고리입니다."}, status=400)

    #         request.user.categories.set(categories)  
    #         return Response({"message": "관심사가 성공적으로 저장되었습니다."}, status=200)
    #     except Exception as e:
    #         return Response({"message": f"에러 발생: {str(e)}"}, status=500)