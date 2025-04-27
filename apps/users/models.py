from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from ..consortia.models import Consortium
from ..municipalities.models import Municipality


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    number_of_phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='Data de Nascimento', null=True, blank=True)
    cpf = models.CharField(
        max_length=14,
        verbose_name='CPF',
        unique=True,  
        null=True,
        blank=True
    )
    city = models.CharField(max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'number_of_phone'
    REQUIRED_FIELDS = ['email', 'username']

    class Meta:
        db_table = 'user'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def type (self):
        if hasattr(self, 'monitor'):
            return Monitor
        elif hasattr(self, 'manager'):
            return Manager
        else:
            return CustomUser


class Monitor(CustomUser):
    municipality = models.OneToOneField(
        Municipality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitor",
        verbose_name="Município"
    )
    consortium = models.ForeignKey(
        Consortium,
        on_delete=models.CASCADE,
        related_name="monitors",
        verbose_name="Consórcio"
    )

    class Meta:
        verbose_name = "Monitor"
        verbose_name_plural = "Monitors"


class Manager(CustomUser):
    consortia = models.ManyToManyField(Consortium, related_name="managers", verbose_name="Consórcios")

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"


class UserResetPassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="password_reset")
    reset_code = models.CharField(max_length=6)
    reset_code_expiration = models.DateTimeField()

    def is_code_valid(self):
        return timezone.now() < self.reset_code_expiration

    def __str__(self):
        return f"Código de {self.user.email} - Expira em {self.reset_code_expiration}"


class TemporaryPassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="temporary_password")
    password = models.CharField(max_length=128)

    def __str__(self):
        return "Temporary password for {self.user.first_name} {self.user.last_name}"