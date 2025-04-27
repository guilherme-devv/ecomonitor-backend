from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Monitor, CustomUser, Manager, UserResetPassword, TemporaryPassword


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'number_of_phone', 'date_of_birth', 'cpf', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'number_of_phone', 'first_name', 'last_name', 'cpf', 'city'),
        }),
    )
    list_display = ('username', 'email', 'number_of_phone', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'number_of_phone', 'first_name', 'last_name', 'cpf')
    ordering = ('username',)


@admin.register(Monitor)
class MonitorAdmin(CustomUserAdmin):
    fieldsets = CustomUserAdmin.fieldsets + (
        ('Monitor Info', {'fields': ('municipality', 'consortium')}),
    )
    list_display = CustomUserAdmin.list_display + ('municipality', 'consortium')


@admin.register(Manager)
class ManagerAdmin(CustomUserAdmin):
    fieldsets = CustomUserAdmin.fieldsets + (
        ('Manager Info', {'fields': ('consortia',)}),
    )
    list_display = CustomUserAdmin.list_display + ('get_consortia',)

    def get_consortia(self, obj):
        return ", ".join([consortium.name for consortium in obj.consortia.all()])
    get_consortia.short_description = "Consortia"


# @admin.register(UserResetPassword)
# class UserResetPasswordAdmin(admin.ModelAdmin):
#     list_display = ('user', 'reset_code', 'reset_code_expiration', 'is_code_valid')
#     readonly_fields = ('reset_code', 'reset_code_expiration', 'is_code_valid')
#     search_fields = ('user__username', 'user__email', 'reset_code')


@admin.register(TemporaryPassword)
class TemporaryPasswordAdmin(admin.ModelAdmin):
    pass