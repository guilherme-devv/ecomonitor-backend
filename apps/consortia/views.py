from .models import Consortium
from rest_framework.viewsets import ModelViewSet
from .serializers import ConsortiumModelSerializer
from rest_framework.permissions import IsAdminUser


class ConsortiumModelViewSet(ModelViewSet):
    
    permission_classes = [IsAdminUser]
    queryset = Consortium.objects.all()
    serializer_class = ConsortiumModelSerializer
