from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'form1', views.Form1ViewSet, basename='recyclable-compositions')


urlpatterns = [
    path('forms/', include(router.urls), name='forms'),
]
