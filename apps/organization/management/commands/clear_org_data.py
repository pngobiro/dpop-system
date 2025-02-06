# apps/organization/management/commands/clear_org_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.organization.models import Department, Role, UserRole

class Command(BaseCommand):
    help = 'Clears all organization data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        UserRole.objects.all().delete()
        Role.objects.all().delete()
        Department.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all organization data'))