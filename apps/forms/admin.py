from django.contrib import admin
from .models import Form1


@admin.register(Form1)
class Form1Admin(admin.ModelAdmin):
    pass
