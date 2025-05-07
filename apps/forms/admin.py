from django.contrib import admin
from .models import RecyclableWasteComposition


@admin.register(RecyclableWasteComposition)
class Form1Admin(admin.ModelAdmin):
    pass
