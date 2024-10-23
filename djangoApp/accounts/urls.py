from django.urls import path
from .views import RegisterAPIView, ObtainTokenPairView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', ObtainTokenPairView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
