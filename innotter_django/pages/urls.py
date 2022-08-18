from django.urls import path, include
from rest_framework import routers
from pages import views


router = routers.DefaultRouter()
router.register('pages', viewset=views.PageViewSet, basename='pages')
router.register('tags', viewset=views.TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls))
]
