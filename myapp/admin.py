from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ContactModel, BuildingPermit, UserHistory

# Register your models here.
# admin.site.register(AdminUser)
admin.site.register(CustomUser)
admin.site.register(ContactModel)
admin.site.register(BuildingPermit)
admin.site.register(UserHistory)

