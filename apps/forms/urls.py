from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'recyclable-waste-composition', views.RecyclableWasteCompositionViewSet, basename='recyclable-compositions')


urlpatterns = [
    path('forms/', include(router.urls), name='forms'),
]
