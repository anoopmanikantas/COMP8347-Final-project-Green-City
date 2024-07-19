from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminUser


# Register your models here.
admin.site.register(AdminUser)
admin.site.register(CustomUser)