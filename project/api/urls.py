from rest_framework import routers
from django.urls import path, include

from .views import FriendRequestViewSet, FriendViewSet


router = routers.DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet)
router.register(r'friends', FriendViewSet, basename='friend')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
