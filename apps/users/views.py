from rest_framework import viewsets
from .models import Monitor
from .serializers import MonitorModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class MonitorModelViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, IsAuthenticated]
    queryset = Monitor.objects.all()
    serializer_class = MonitorModelSerializer


    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny(),]
        return super().get_permissions()
