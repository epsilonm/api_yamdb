from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework import routers

from api.views import UsersViewSet, UserCreateView, UserJWTTokenCreateView

router_version_1 = routers.DefaultRouter()
router_version_1.register(r'users', UsersViewSet, basename='users')
router_version_1.register(r'categories', CategoryViewSet)
router_version_1.register(r'genres', GenreViewSet)
router_version_1.register(r'titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router_version_1.urls)),
    path('v1/auth/signup/', UserCreateView.as_view()),
    path('v1/auth/token/', UserJWTTokenCreateView.as_view()),
    ]
