from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_superuser','is_banned']

admin.site.register(CustomUser, CustomUserAdmin)