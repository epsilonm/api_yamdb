from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from http import HTTPStatus
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format=('%(asctime)s, %(levelname)s, '
            ' %(message)s, '
            'in function: %(funcName)s, '
            'line: %(lineno)d'),
    filename='example.log', encoding='utf-8'
    )

from django.contrib.auth.tokens import default_token_generator

from users.models import User
from .serializers import UsersSerializer, CreateUserSerializer, UserJWTTokenCreateSerializer


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination


class UserCreateView(APIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserJWTTokenCreateView(APIView):
    serializer_class = UserJWTTokenCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            logging.info(serializer.data)
            confirmation_code = serializer.data.get('confirmation_code')
            username = serializer.data.get('username')
            logging.info(f'username - {username}, confirmation code - {confirmation_code}')
            if User.objects.filter(username=username, confirmation_code=confirmation_code).exists():
                logging.info(f'user{request.user}')
                token = AccessToken.for_user(User.objects.get(username=username, confirmation_code=confirmation_code))
                return Response(data={'token': str(token)}, status=200)
            return Response('Username or confirmation_code are not correct', status=400)
        return Response(data=serializer.errors, status=400)
