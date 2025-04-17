from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from djoser.views import UserViewSet
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response

class CustomUserViewSet(UserViewSet):
    queryset=CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

    # def get(self, request):
    #     users=CustomUser.objects.all()
    #     serializer=UserSerializer(users, many=True)
    #     return Response(serializer.data) 