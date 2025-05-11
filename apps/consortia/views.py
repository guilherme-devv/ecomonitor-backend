from .models import Consortium
from rest_framework.viewsets import ModelViewSet
from .serializers import ConsortiumModelSerializer
from rest_framework.permissions import AllowAny
from ..users.serializers import MonitorModelSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from ..users.models import Monitor
from ..users.serializers import MonitorModelSerializer
from django.db.models import Sum
from datetime import timedelta, date
from ..forms.models import RecyclableWasteComposition


class ConsortiumModelViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Consortium.objects.all()
    serializer_class = ConsortiumModelSerializer

    @action(detail=True, methods=['get'], url_path='monitors', url_name='monitors')
    def get_monitors(self, request, pk=None):
        """
        Retorna os monitores associados a um consórcio específico.
        """
        consortium = self.get_object()
        monitors = Monitor.objects.filter(consortium=consortium)
        serializer = MonitorModelSerializer(monitors, many=True)
        return Response(serializer.data)
    
    def get_date_interval(self, request):
            period = request.query_params.get('period', 'day')

            if period == 'custom':
                start_date = request.query_params.get('start_date')
                end_date = request.query_params.get('end_date')
                start_date = date.fromisoformat(start_date)
                end_date = date.fromisoformat(end_date)
            
            elif period == 'day':
                end_date = date.today()
                start_date = date.today()
            
            elif period == 'week':
                today = date.today()
                days_since_sunday = today.weekday()
                start_date = today - timedelta(days=days_since_sunday)
                end_date = date.today()
            
            elif period == 'month':
                today = date.today()
                start_date = today.replace(day=1)
                end_date = date.today()
            
            return start_date, end_date

    @action(detail=True, methods=['get'], url_path='waste-summary', url_name='waste-summary')
    def get_waste_summary(self, request, pk=None):
        """
            Retorna um resumo dos resíduos coletados por todos os monitores de um consórcio específico.
            query_params:
                - start_date: Data inicial para o resumo (formato YYYY-MM-DD).
                - end_date: Data final para o resumo (formato YYYY-MM-DD).
                - period: Período para o resumo ('day', 'week', 'month'). Padrão é 'day'.
            response:
                - total_waste: Total de resíduos coletados no período.
                - previous_day_comparison: Comparação com o dia anterior.
                - previous_week_comparison: Comparação com a semana anterior.
        """

        start_date, end_date = self.get_date_interval(request)

        consortium = self.get_object()

        total_waste = RecyclableWasteComposition.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            consortium=consortium
        ).aggregate(total=Sum('total'))['total'] or 0

        previous_day = date.today() - timedelta(days=1)
        previous_day_waste = RecyclableWasteComposition.objects.filter(
            created_at__date=previous_day,
            consortium=consortium
        ).aggregate(total=Sum('total'))['total'] or 0

        previous_week_start = date.today() - timedelta(days=date.today().weekday() + 7)
        previous_week_end = previous_week_start + timedelta(days=6)
        previous_week_waste = RecyclableWasteComposition.objects.filter(
            created_at__date__gte=previous_week_start,
            created_at__date__lte=previous_week_end,
            consortium=consortium
        ).aggregate(total=Sum('total'))['total'] or 0

        response_data = {
            "total_waste": round(total_waste, 2),
            "previous_day_comparison": round(total_waste - previous_day_waste, 2),
            "previous_week_comparison": round(total_waste - previous_week_waste, 2),
        }

        return Response(response_data, status=200)
    
    @action(detail=True, methods=['get'], url_path='waste-gravimetry', url_name='waste-gravimetry')
    def get_waste_gravimetry(self, request, pk=None):
        consortium = self.get_object()

        gravimetry = RecyclableWasteComposition.objects.filter(
            created_at__date = date.today(),
            consortium=consortium
        ).aggregate(total=Sum('total'))['total'] or 0

        return Response({
            'tailings': 0,
            'recyclable': round(gravimetry, 2),
            'organic': 0,
            'total': round(gravimetry, 2),
        }, status=200)
    
    @action(detail=True, methods=['get'], url_path='total-recyclable-waste', url_name='total-recyclable-waste')
    def get_yearly_waste_gravimetry(self, request, pk=None):
        consortium = self.get_object()

        total_wastes = RecyclableWasteComposition.objects.filter(
                created_at__year=date.today().year,
                consortium=consortium
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
