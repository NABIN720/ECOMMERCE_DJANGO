from django.contrib import admin
# from .models import CustomUser

# Register your models here.
# admin.site.register(CustomUser)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)