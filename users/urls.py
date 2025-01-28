from django.urls import path
from .views import ProtectedView

urlpatterns = [
    path('protected-endpoint/', ProtectedView.as_view(), name='protected-endpoint'),
]
