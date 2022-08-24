from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from users.views import UserViewSet
from posts.views import PostViewSet
from pages.views import PageViewSet, TagViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="Innotter",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()
router.register('users', viewset=UserViewSet, basename='users')
router.register('pages', viewset=PageViewSet, basename='pages')
router.register('posts', viewset=PostViewSet, basename='posts')
router.register('tags', viewset=TagViewSet, basename='tags')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
