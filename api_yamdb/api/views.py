from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from http import HTTPStatus
import logging

from users.models import User
from .serializers import UsersSerializer, CreateUserSerializer, UserJWTTokenCreateSerializer, UserPatchSerializer
from .permissions import IsAdmin, IsUser

logging.basicConfig(
    level=logging.DEBUG,
    format=('%(asctime)s, %(levelname)s, '
            ' %(message)s, '
            'in function: %(funcName)s, '
            'line: %(lineno)d'),
    filename='example.log')

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UsersSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me',
            serializer_class=UserPatchSerializer)
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


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
            confirmation_code = serializer.data.get('confirmation_code')
            username = serializer.data.get('username')
            if User.objects.filter(username=username).exists():
                if User.objects.filter(username=username,
                                       confirmation_code=confirmation_code).exists():
                    user = User.objects.get(username=username, confirmation_code=confirmation_code)
                    token = AccessToken.for_user(user)
                    return Response(data={'token': str(token)}, status=HTTPStatus.OK)
                return Response('Confirmation code is incorrect!', status=HTTPStatus.BAD_REQUEST)
            return Response('User with this username does not exist', status=HTTPStatus.NOT_FOUND)
        return Response(data=serializer.errors, status=HTTPStatus.BAD_REQUEST)
