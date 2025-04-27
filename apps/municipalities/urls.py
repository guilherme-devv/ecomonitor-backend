from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'', MunicipalityModelViewSet, 'municipalities')

urlpatterns = [
    path(r'municipalities/', include((router.urls, 'municipalities'))),
]
