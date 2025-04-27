from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from apps.users.models import Monitor, TemporaryPassword
from django.dispatch import Signal


monitor_created_signal = Signal()

@receiver(monitor_created_signal, sender=Monitor)
def send_password_email(sender, instance, **kwargs):
    password = kwargs.get('password')
    TemporaryPassword.objects.create(
        user=instance,
        password=password
    )
