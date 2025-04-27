from django.contrib import admin
from .models import Consortium


@admin.register(Consortium)
class ConsortiaAdmin(admin.ModelAdmin):
    pass
