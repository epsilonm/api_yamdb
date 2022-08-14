from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets, mixins, permissions

from users.models import User
from reviews.models import Category, Genre, Title, Review
from .permissions import IsAdmin
from .serializers import (UsersSerializer, CreateUserSerializer,
                          UserJWTTokenCreateSerializer, UserPatchSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer
                          )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UsersSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserJWTTokenCreateView(APIView):
    serializer_class = UserJWTTokenCreateSerializer
    permission_classes = [permissions.AllowAny]

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


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    # def perform_create(self, serializer):
    #     post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
    #     serializer.save(author=self.request.user, post=post)
