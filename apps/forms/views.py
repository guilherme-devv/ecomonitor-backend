from rest_framework import viewsets
from apps.forms.models import RecyclableWasteComposition
from apps.forms.serializers import RecyclableWasteCompositionModelSerializer
from rest_framework.response import Response
from apps.users.permissions import IsMonitor
from rest_framework.permissions import IsAuthenticated 

class RecyclableWasteCompositionViewSet(viewsets.ModelViewSet):
    queryset = RecyclableWasteComposition.objects.all()
    serializer_class = RecyclableWasteCompositionModelSerializer
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
