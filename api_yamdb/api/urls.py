from django.urls import include, path
from rest_framework import routers

from api.views import UsersViewSet, UserCreateView, UserJWTTokenCreateView

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserCreateView.as_view()),
    path('v1/auth/token/', UserJWTTokenCreateView.as_view()),
    ]
