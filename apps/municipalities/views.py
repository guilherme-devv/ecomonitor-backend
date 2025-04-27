from rest_framework.viewsets import ModelViewSet
from .models import Municipality
from .serializers import MunicipalityModelSerializer


class MunicipalityModelViewSet(ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalityModelSerializer
