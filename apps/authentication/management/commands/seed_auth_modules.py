from django.core.management.base import BaseCommand
from apps.home.models import Module

class Command(BaseCommand):
    help = 'Seeds authentication related modules'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding authentication modules...')

        auth_modules = [
            {
                'name': 'User Management',
                'description': 'Manage user accounts and permissions',
                'icon_class': 'fas fa-users',
                'url_name': 'authentication:user_list',
                'permission_codename': 'access_user_management'
            },
            {
                'name': 'Access Control',
                'description': 'Manage roles and permissions',
                'icon_class': 'fas fa-user-shield',
                'url_name': 'authentication:permissions',
                'permission_codename': 'access_permissions'
            },
        ]

        for module_data in auth_modules:
            module, created = Module.objects.get_or_create(
                name=module_data['name'],
                defaults={
                    'description': module_data['description'],
                    'icon_class': module_data['icon_class'],
                    'url_name': module_data['url_name'],
                    'permission_codename': module_data['permission_codename']
                }
            )

            if created:
                self.stdout.write(f"Created module: {module.name}")
            else:
                self.stdout.write(self.style.WARNING(f"Module '{module.name}' already exists. Skipping."))

        self.stdout.write(self.style.SUCCESS('Successfully seeded authentication modules'))