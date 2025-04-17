from django.urls import path
from .views import CustomUserViewSet

urlpatterns = [
    path('', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
]