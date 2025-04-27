from rest_framework import serializers
from .models import Form1


class Form1ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form1
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'municipality': {'read_only': True},
            'consortium': {'read_only': True},
        }


    def save(self, **kwargs):
        user = self.context['request'].user
        self.validated_data['consortium'] = user.monitor.consortium
        self.validated_data['municipality'] = user.monitor.municipality
        self.validated_data['user'] = user.monitor
        return super().save(**kwargs)