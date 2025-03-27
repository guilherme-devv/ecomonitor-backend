from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        (1, 'Monitor'),
        (2, 'Gestor'),
    )

    email = models.EmailField(max_length=255, unique=True)
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
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=1)
    city = models.CharField(max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'number_of_phone'
    REQUIRED_FIELDS = ['email', 'username']

    class Meta:
        db_table = 'user'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self) -> str:
        return self.username
    
class UserResetPassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="password_reset")
    reset_code = models.CharField(max_length=6)
    reset_code_expiration = models.DateTimeField()

    def is_code_valid(self):
        """Verifica se o código ainda é válido."""
        return timezone.now() < self.reset_code_expiration

    def __str__(self):
        return f"Código de {self.user.email} - Expira em {self.reset_code_expiration}"
