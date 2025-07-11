# Generated by Django 4.2.13 on 2025-02-06 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "icon_class",
                    models.CharField(
                        blank=True,
                        help_text="Font Awesome icon class (e.g., 'fas fa-file-alt')",
                        max_length=100,
                    ),
                ),
                (
                    "url_name",
                    models.CharField(
                        blank=True,
                        help_text="Name of the URL pattern for this module (e.g., 'document_module_view')",
                        max_length=200,
                    ),
                ),
                (
                    "permission_codename",
                    models.CharField(
                        blank=True,
                        help_text="Codename for permission to access this module (e.g., 'access_documents')",
                        max_length=150,
                        unique=True,
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modules",
                        to="organization.department",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "permissions": [],
            },
        ),
    ]
