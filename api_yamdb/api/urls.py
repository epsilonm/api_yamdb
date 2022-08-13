from rest_framework import routers

from django.urls import include, path

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router_version_1 = routers.DefaultRouter()
router_version_1.register(r'categories', CategoryViewSet)
router_version_1.register(r'genres', GenreViewSet)
router_version_1.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_version_1.urls))
]
