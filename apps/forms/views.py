from rest_framework import viewsets
from apps.forms.models import Form1
from apps.forms.serializers import Form1ModelSerializer
from rest_framework.response import Response
from apps.users.permissions import IsMonitor
from rest_framework.permissions import IsAuthenticated 

class Form1ViewSet(viewsets.ModelViewSet):
    queryset = Form1.objects.all()
    serializer_class = Form1ModelSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsMonitor(),]
        return super().get_permissions()
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
