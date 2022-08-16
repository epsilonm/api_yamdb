from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, viewsets, mixins

from reviews.models import Category, Genre, Title

from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ("name",)
    filter_backends = (filters.SearchFilter,)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name",)
    filter_backends = (filters.SearchFilter,)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
