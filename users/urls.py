from django.urls import path
from .views import ProtectedView, ProfileView, RegisterUserView

urlpatterns = [
    path('protected-endpoint/', ProtectedView.as_view(), name='protected-endpoint'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterUserView.as_view(), name='register'),
]
