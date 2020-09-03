from rest_framework import generics, status, filters
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, LoginSerializer
from rest_framework.response import Response



class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)
