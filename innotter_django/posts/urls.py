from django.urls import path, include
from rest_framework import routers
from posts import views


router = routers.DefaultRouter()
router.register('posts', viewset=views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls))
]
