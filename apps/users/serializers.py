from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser, Monitor
from .signals import monitor_created_signal
from ..forms.models import RecyclableWasteComposition
from ..forms.serializers import RecyclableWasteCompositionModelSerializer

class BaseCustomUserSerializer(serializers.ModelSerializer):

    def validate_cpf(self, value):
        if CustomUser.objects.filter(cpf=value).exists():
            raise serializers.ValidationError('Um usuário com este CPF já existe.')
        return value

    def validate_number_of_phone(self, value):
        if CustomUser.objects.filter(number_of_phone=value).exists():
            raise serializers.ValidationError('Um usuário com este número de telefone já existe.')
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Um usuário com este email já existe.')
        return value


class MonitorModelSerializer(BaseCustomUserSerializer):
    last_form = serializers.SerializerMethodField()
    total_collected = serializers.SerializerMethodField()

    class Meta:
        model = Monitor
        fields = [
            'id','number_of_phone', 'email', 'first_name', 'last_name', 
            'city', 'cpf', 'date_of_birth', 'consortium', 'municipality',
            'last_form', 'total_collected'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'password': {'write_only': True},
            'consortium': {'required': False},
            'municipality': {'required': False}
        }
    
    def get_last_form(self, obj):
        last_form = RecyclableWasteComposition.objects.filter(user=obj).order_by('-created_at').first()
        if last_form:
            return RecyclableWasteCompositionModelSerializer(last_form).data
        return None
    
    def get_total_collected(self, obj):
        total_collected = sum(RecyclableWasteComposition.objects.filter(user=obj).values_list('total', flat=True))
        return total_collected

    def create(self, validated_data):
        password = self.random_password()
        validated_data['password'] = make_password(password)
        # validated_data['consortium'] = validated_data['municipality'].consortium
        instance = super().create(validated_data)
        monitor_created_signal.send(sender=Monitor, instance=instance, password=password)
        return instance
    
    def random_password(self):
        from uuid import uuid4
        return uuid4().hex[:8]
