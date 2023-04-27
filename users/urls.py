from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserDetailAPIView, UserCreateAPIView, UserUpdateAPIView, UserDestroyAPIView, UserListAPIView

urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),
    path('<int:pk>/update/', UserUpdateAPIView.as_view()),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
