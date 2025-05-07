from rest_framework import serializers
from .models import RecyclableWasteComposition


class RecyclableWasteCompositionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableWasteComposition
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'municipality': {'read_only': True},
            'consortium': {'read_only': True},
            'total': {'read_only': True},
        }


    def save(self, **kwargs):
        user = self.context['request'].user
        self.validated_data['consortium'] = user.monitor.consortium
        self.validated_data['municipality'] = user.monitor.municipality
        self.validated_data['user'] = user.monitor
        self.validated_data['total'] = sum([
            self.validated_data.get('quantity_tetrapak', 0),
            self.validated_data.get('quantity_aluminum', 0),
            self.validated_data.get('quantity_white_paper', 0),
            self.validated_data.get('quantity_colored_paper', 0),
            self.validated_data.get('quantity_cardboard', 0),
            self.validated_data.get('quantity_newspaper', 0),
            self.validated_data.get('quantity_general_plastic', 0),
            self.validated_data.get('quantity_film_plastic', 0),
            self.validated_data.get('quantity_pet', 0),
            self.validated_data.get('quantity_pvc', 0)
        ])
        self.validated_data['total'] = round(self.validated_data['total'], 2)
        return super().save(**kwargs)