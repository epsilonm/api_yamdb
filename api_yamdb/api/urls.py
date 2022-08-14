from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet)
from django.urls import include, path
from rest_framework import routers

from api.views import UsersViewSet, UserCreateView, UserJWTTokenCreateView

router_version_1 = routers.DefaultRouter()
router_version_1.register(r'users', UsersViewSet, basename='users')
router_version_1.register(r'categories', CategoryViewSet, basename='categories')
router_version_1.register(r'genres', GenreViewSet, basename='genres')
router_version_1.register(r'titles', TitleViewSet, basename='titles')
router_version_1.register(r'titles/(?P<title_id>\d+)/reviews',
                          ReviewViewSet, basename='reviews')


urlpatterns = [
    path('v1/', include(router_version_1.urls)),
    path('v1/auth/signup/', UserCreateView.as_view()),
    path('v1/auth/token/', UserJWTTokenCreateView.as_view()),
    ]
