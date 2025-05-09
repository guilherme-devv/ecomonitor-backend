from rest_framework.viewsets import ModelViewSet
from .models import Municipality
from .serializers import MunicipalityModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..forms.models import RecyclableWasteComposition
from django.db.models import Sum
from datetime import date


class MunicipalityModelViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Municipality.objects.all()
    serializer_class = MunicipalityModelSerializer

    @action(detail=True, methods=['get'], url_path='waste-gravimetry', url_name='waste-gravimetry')
    def get_waste_gravimetry(self, request, pk=None):
        municipality = self.get_object()

        gravimetry = RecyclableWasteComposition.objects.filter(
            created_at__date = date.today(),
            municipality=municipality
        ).aggregate(total=Sum('total'))['total'] or 0

        return Response({
            'tailings': 0,
            'recyclable': round(gravimetry, 2),
            'organic': 0,
            'total': round(gravimetry, 2),
        }, status=200)
    
    @action(detail=True, methods=['get'], url_path='total-recyclable-waste', url_name='total-recyclable-waste')
    def get_yearly_waste_gravimetry(self, request, pk=None):
        municipality = self.get_object()

        total_wastes = RecyclableWasteComposition.objects.filter(
                created_at__year=date.today().year,
                municipality=municipality
            ).aggregate(total=Sum('total'), 
                    quantity_tetrapak=Sum('quantity_tetrapak'), 
                    quantity_aluminum=Sum('quantity_aluminum'), 
                    quantity_white_paper=Sum('quantity_white_paper'), 
                    quantity_colored_paper=Sum('quantity_colored_paper'), 
                    quantity_cardboard=Sum('quantity_cardboard'), 
                    quantity_newspaper=Sum('quantity_newspaper'), 
                    quantity_general_plastic=Sum('quantity_general_plastic'), 
                    quantity_film_plastic=Sum('quantity_film_plastic'), 
                    quantity_pet=Sum('quantity_pet'), 
                    quantity_pvc=Sum('quantity_pvc'))
    
        return Response(total_wastes, status=200)
