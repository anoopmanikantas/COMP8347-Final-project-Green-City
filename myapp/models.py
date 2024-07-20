# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid


# class AdminUser(AbstractUser):
#     contact_number = models.CharField(max_length=50, blank=True, null=True)
#
#     groups = models.ManyToManyField(
#         Group,
#         related_name='adminuser_set',
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='adminuser_permissions_set',
#         blank=True
#     )
#
#     def _str_(self):
#         return self.username


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username


class BuildingPermit(models.Model):
    AREA_CHOICES = [
        ('0-0.3', '0<0.3'),
        ('0.3-0.5', '0.3<0.5'),
        ('0.5-0.7', '0.5<0.7'),
        ('0.7+', '>=0.7'),
    ]

    FLOORS_CHOICES = [
        ('1-3', '1-3'),
        ('4-6', '4-6'),
        ('7+', '>=7'),
    ]

    __application_status_options = {
        "submitted": "Submitted",
        "in progress": "In Progress",
        "approved": "Approved",
    }

    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    mail_id = models.EmailField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    floors = models.CharField(max_length=20, choices=FLOORS_CHOICES)
    government_id_proof = models.FileField(upload_to='id_proofs/')
    land_purchase_record = models.FileField(upload_to='land_records/')
    trees_required = models.PositiveIntegerField()
    application_number = models.CharField(max_length=50, default=str(uuid.uuid4()))
    application_status = models.CharField(max_length=20, choices=__application_status_options, default="submitted")

    def __str__(self):
        return f"Building Permit for {self.name}"
