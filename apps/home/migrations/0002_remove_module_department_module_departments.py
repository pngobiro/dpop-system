# Generated by Django 4.2.13 on 2025-02-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0002_role_permissions"),
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="module",
            name="department",
        ),
        migrations.AddField(
            model_name="module",
            name="departments",
            field=models.ManyToManyField(
                blank=True, related_name="modules", to="organization.department"
            ),
        ),
    ]
