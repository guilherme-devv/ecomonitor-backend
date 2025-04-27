from django.urls import path, include, re_path
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.contrib import admin
from drf_yasg import openapi
from rest_framework import views, status
from rest_framework.response import Response


schema_view = get_schema_view(
    openapi.Info(
        title=settings.PROJECT_NAME,
        default_version='v1',
        description="Este documento descreve os recursos disponíveis nesta API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


class HealthCheckView(views.APIView):
    schema = None
    
    def get(self, request):
        return Response({"application": "running"}, status=status.HTTP_200_OK)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health_check/', HealthCheckView.as_view(), name='health_check'),

    path(r'api/', include('apps.accounts.urls')),
    path(r'api/', include('apps.users.urls')),
    path(r'api/', include('apps.consortia.urls')),
    path(r'api/', include('apps.municipalities.urls')),
    path(r'api/', include('apps.forms.urls')),

    re_path(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


