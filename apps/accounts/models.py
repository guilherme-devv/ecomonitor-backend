from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import secrets


SMS_CODE_TIMEOUT = 300

User = get_user_model()

class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=15, default="00000000000")
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'verification_code'
        verbose_name = 'Código de Verificação'
        verbose_name_plural = 'Códigos de Verificação'


    def __str__(self):
        return f"Código {self.code} para {self.phone_number}"
    
    def is_valid_code(self):
        return self.is_valid and (now() - self.timestamp).total_seconds() < SMS_CODE_TIMEOUT
    
    def invalidate_code(self):
        self.is_valid = False
        self.save()

    def check_code(self, code):
        return self.code == code

    @staticmethod
    def invalidate_all_codes(phone_number):
        VerificationCode.objects.filter(phone_number=phone_number).update(is_valid=False)

    @staticmethod
    def generate_verification_code():
        return str(secrets.randbelow(1000000)).zfill(6)
