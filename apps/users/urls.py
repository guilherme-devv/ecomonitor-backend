from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'', CustomUserViewSet, 'users')

urlpatterns = [
    path(r'users/', include((router.urls, 'users'))),
]
