from django.urls import path, include
from rest_framework import routers
from users import views


router = routers.DefaultRouter()
router.register('users', viewset=views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
]
