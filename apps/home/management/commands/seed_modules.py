from django.core.management.base import BaseCommand
from apps.home.models import Module
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Seeds initial modules data into the database, including permissions'

    def handle(self, *args, **options):
        self.stdout.write('Seeding modules data with permissions...')

        modules_data = [
            {'name': 'Documents', 'description': 'Manage and organize department documents.', 'icon_class': 'fas fa-file-alt', 'url_name': '#', 'permission_codename': 'access_documents_module'}, # Added permission_codename
            {'name': 'DCRT', 'description': 'Access and analyze DCRT data and statistics.', 'icon_class': 'fas fa-chart-bar', 'url_name': '#', 'permission_codename': 'access_dcrt_module'}, # Added permission_codename
            {'name': 'Meetings', 'description': 'Schedule and manage department meetings.', 'icon_class': 'fas fa-calendar-alt', 'url_name': '#', 'permission_codename': 'access_meetings_module'}, # Added permission_codename
            {'name': 'Tasks', 'description': 'Create, assign, and track department tasks.', 'icon_class': 'fas fa-tasks', 'url_name': '#', 'permission_codename': 'access_tasks_module'}, # Added permission_codename
            {'name': 'Reports', 'description': 'Generate and view department reports.', 'icon_class': 'fas fa-file-pdf', 'url_name': '#', 'permission_codename': 'access_reports_module'}, # Added permission_codename
            {'name': 'Budget', 'description': 'Manage and track department budgets.', 'icon_class': 'fas fa-money-bill-alt', 'url_name': '#', 'permission_codename': 'access_budget_module'}, # Added permission_codename
            {'name': 'Workplans', 'description': 'Plan and monitor department workplans.', 'icon_class': 'fas fa-clipboard-list', 'url_name': '#', 'permission_codename': 'access_workplans_module'}, # Added permission_codename
            {'name': 'Surveys', 'description': 'Create and analyze department surveys.', 'icon_class': 'fas fa-poll', 'url_name': '#', 'permission_codename': 'access_surveys_module'}, # Added permission_codename
            {'name': 'Memos', 'description': 'Create and manage department memos.', 'icon_class': 'fas fa-envelope', 'url_name': '#', 'permission_codename': 'access_memos_module'}, # Added permission_codename
        ]

        # Dynamically define permissions in Module._meta.permissions
        module_permissions = []
        for module_data in modules_data:
            permission_codename = module_data['permission_codename']
            permission_name = f"Can access {module_data['name']} module" # User-friendly permission name
            module_permissions.append((permission_codename, permission_name))

        Module._meta.permissions = module_permissions # Set custom permissions for the Module model


        for module_data in modules_data:
            Module.objects.get_or_create(
                name=module_data['name'],
                defaults={
                    'description': module_data['description'],
                    'icon_class': module_data['icon_class'],
                    'url_name': module_data['url_name'],
                    'permission_codename': module_data['permission_codename'], # Set permission_codename during creation
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Created module: {module_data['name']} with permission: {module_data['permission_codename']}"))

        self.stdout.write(self.style.SUCCESS('Successfully seeded modules data and defined permissions.'))