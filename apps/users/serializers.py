from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import CustomUser

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


class CreateCustomUserModelSerializer(BaseCustomUserSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'number_of_phone', 'email', 'first_name', 'last_name', 
            'city', 'cpf', 'date_of_birth', 'password', 'type'
        ]

    def save(self, **kwargs):
        if self.validated_data.get('password', None):
            self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)


class CustomUserModelSerializer(BaseCustomUserSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'number_of_phone', 'email', 'first_name', 'last_name', 
            'city', 'cpf', 'date_of_birth'
        ]