from http import HTTPStatus
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, mixins, permissions, filters, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
from .serializers import (UsersSerializer, CreateUserSerializer,
                          UserJWTTokenCreateSerializer,
                          CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitlesEditorSerializer, TitlesReadSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UsersSerializer
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    pagination_class = LimitOffsetPagination

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save(role=self.request.user.role)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_create_view(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        queryset = User.objects.filter(email=email, username=username)
        if not queryset.exists():
            serializer.save()
            confirmation_code = default_token_generator.make_token(
                User(email=email, username=username)
            )
            message = (f'Здравствуйте, {username}! '
                       f'Ваш код подтверждения: {confirmation_code}')
            send_mail(message=message,
                      subject='Confirmation code',
                      recipient_list=[email],
                      from_email=None)
            return Response(serializer.data, status=HTTPStatus.OK)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class UserJWTTokenCreateView(generics.CreateAPIView):
    serializer_class = UserJWTTokenCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perfom_create(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            confirmation_code = serializer.data.get('confirmation_code')
            username = serializer.data.get('username')
            if User.objects.filter(username=username).exists():
                if User.objects.filter(
                        username=username,
                        confirmation_code=confirmation_code
                ).exists():
                    user = User.objects.get(
                        username=username,
                        confirmation_code=confirmation_code
                    )
                    token = AccessToken.for_user(user)
                    return Response(
                        data={'token': str(token)},
                        status=HTTPStatus.OK
                    )
                return Response(
                    'Confirmation code is incorrect!',
                    status=HTTPStatus.BAD_REQUEST
                )
            return Response(
                'User with this username does not exist',
                status=HTTPStatus.NOT_FOUND
            )
        return Response(
            data=serializer.errors,
            status=HTTPStatus.BAD_REQUEST
        )


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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesEditorSerializer
        return TitlesReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get("review_id"),
            title__pk=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
