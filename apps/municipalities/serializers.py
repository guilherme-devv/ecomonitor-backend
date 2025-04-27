from rest_framework import serializers
from .models import Municipality


class MunicipalityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.consortium is None:
            instance.monitor = None
            instance.save()
        return instance
