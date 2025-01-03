from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User

class UserAPIView(APIView):
    def get(self, request, username):
        if request.user.is_authenticated:
            user=get_object_or_404(User, username=username)
            serializer=UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
