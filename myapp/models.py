# models.py
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# from myapp import forms
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
    is_admin = models.BooleanField(default=False)

    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='CustomUser_set',
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='CustomUser_permissions_set',
    #     blank=True
    # )

    def __str__(self):
        return self.username


class ContactModel(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=10, blank=True, null=True)


def user_id_proof_path(instance, filename):
    return f'id_proofs/{instance.usr.id}/{filename}'


def user_land_records_path(instance, filename):
    return f'land_records/{instance.usr.id}/{filename}'


def user_additional_document_1_path(instance, filename):
    return f'additional_records_1/{instance.usr.id}/{filename}'


def user_additional_records_2_path(instance, filename):
    return f'additional_records_2/{instance.usr.id}/{filename}'


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
        "rejected": "Rejected",
        "additional": "Additional Document Required",
    }

    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    mail_id = models.EmailField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    floors = models.CharField(max_length=20, choices=FLOORS_CHOICES)
    government_id_proof = models.FileField(upload_to=user_id_proof_path)
    land_purchase_record = models.FileField(upload_to=user_land_records_path)
    trees_required = models.PositiveIntegerField()
    application_number = models.CharField(max_length=50, default=str(uuid.uuid4()))
    application_status = models.CharField(max_length=20, choices=__application_status_options, default="submitted")
    date = models.CharField(max_length=50, default=str(datetime.now().strftime("%B %d, %Y")))
    user_id = models.PositiveIntegerField(default=1)
    usr = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    additional_document_description = models.CharField(max_length=1000, blank=True, null=True)
    additional_document_1 = models.FileField(upload_to=user_additional_document_1_path, blank=True, null=True)
    additional_document_2 = models.FileField(upload_to=user_additional_records_2_path, blank=True, null=True)

    def __str__(self):
        return f"Building Permit for {self.name}"


class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    visits = models.PositiveIntegerField(default=0)
    visit_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} visited {self.visits} time(s) on {self.visit_date}"
