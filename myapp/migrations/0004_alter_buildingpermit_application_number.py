# Generated by Django 4.1 on 2024-07-25 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_alter_buildingpermit_application_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buildingpermit",
            name="application_number",
            field=models.CharField(
                default="2816d512-ba27-4558-b758-d90aa022fa7f", max_length=50
            ),
        ),
    ]
