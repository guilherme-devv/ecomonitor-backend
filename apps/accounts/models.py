from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_codes")
    code = models.CharField(max_length=64)  # Alterado de 6 para 64
    created_at = models.DateTimeField(default=now)
    is_valid = models.BooleanField(default=True)

    class Meta:
        db_table = 'verification_code'
        verbose_name = 'Código de Verificação'
        verbose_name_plural = 'Códigos de Verificação'


    def __str__(self):
        return f"Código {self.code} para {self.user.number_of_phone}"
