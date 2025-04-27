from rest_framework import serializers
from .models import Consortium


class ConsortiumModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consortium
        fields = '__all__'
