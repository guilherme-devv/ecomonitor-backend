from datetime import datetime
from django.contrib.auth.models import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, RefreshToken)
from apps.users.models import CustomUser, Manager, Monitor


class RecoveryPasswordResponseSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=30)
    new_password = serializers.CharField(max_length=30)


class TokenObtainPairSerializerCustom(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = TokenUserSerializer(self.user)
        data['user'] = serializer.data
        return data


class TokenUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    consortium = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_consortium(self, obj):
        if obj.type == Manager:
            consortium = Manager.objects.get(id=obj.id).consortia
            return consortium.id if consortium else None
        elif obj.type == Monitor:
            consortium = Monitor.objects.get(id=obj.id).consortium
            return consortium.id if consortium else None
        return None

    def get_type(self, obj):
        if obj.type == Manager:
            return 'manager'
        elif obj.type == Monitor:
            return 'monitor'
        return 'user'

class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = TokenUserSerializer()


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['new_password']

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()

    def to_representation(self, instance):
        return {'new_password': self.validated_data['new_password']}


class ChangePasswordResponseSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=30)


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError("O número deve estar no formato internacional (+55 para Brasil).")
        return value


class VerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate_phone_number(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError("O número deve estar no formato internacional (+55 para Brasil).")
        if not value[1:].isdigit():
            raise serializers.ValidationError("O número de telefone deve conter apenas dígitos.")
        return value

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("O código de verificação deve ter exatamente 6 dígitos numéricos.")
        return value
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário com este e-mail não existe.")
        return value


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.CharField(max_length=6)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário com este e-mail não existe.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário com este e-mail não existe.")
        return value
