from django.contrib import admin
from .models import Municipality


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    pass