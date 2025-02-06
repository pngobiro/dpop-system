# apps/home/management/commands/seed_modules.py
from django.core.management.base import BaseCommand
from apps.home.models import Module
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Seeds modules and their permissions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding modules and permissions...')

        # Delete existing modules
        Module.objects.all().delete()

        modules_data = [
            {
                'name': 'Document Management',
                'description': 'Create, share and manage electronic documents', 
                'icon_class': 'fas fa-file-alt',
                'url_name': 'document_management:document_list',
                'permission_codename': 'access_documents'
            },
            {
                'name': 'Meetings',
                'description': 'Schedule and manage meetings',
                'icon_class': 'fas fa-calendar-alt',
                'url_name': 'meetings:dashboard',
                'permission_codename': 'access_meetings'
            },
            {
                'name': 'Budget',
                'description': 'Manage workplans and budgets',
                'icon_class': 'fas fa-money-bill-alt',
                'url_name': 'budget:workplan_summary',
                'permission_codename': 'access_budget'
            },
            {
                'name': 'Statistics',
                'description': 'Access and analyze DCRT data',
                'icon_class': 'fas fa-chart-bar',
                'url_name': 'statistics:home',
                'permission_codename': 'access_statistics'
            },
            {
                'name': 'Performance',
                'description': 'Performance tracking and reporting',
                'icon_class': 'fas fa-tachometer-alt',
                'url_name': 'performance:dashboard',
                'permission_codename': 'access_performance'
            },
            {
                'name': 'Memos',
                'description': 'Internal memos and communications',
                'icon_class': 'fas fa-envelope',
                'url_name': 'memos:department_dashboard',
                'permission_codename': 'access_memos'
            },
            {
                'name': 'Projects',
                'description': 'Track transformative initiatives',
                'icon_class': 'fas fa-project-diagram',
                'url_name': 'projects:dashboard',
                'permission_codename': 'access_projects'
            },
            {
                'name': 'Reports',
                'description': 'Generate and download reports',
                'icon_class': 'fas fa-file-pdf',
                'url_name': 'reports:dashboard', 
                'permission_codename': 'access_reports'
            }
        ]

        # Get content type for Module model
        content_type = ContentType.objects.get_for_model(Module)

        # Create modules and permissions
        for module_data in modules_data:
            # Create module
            module = Module.objects.create(
                name=module_data['name'],
                description=module_data['description'],
                icon_class=module_data['icon_class'],
                url_name=module_data['url_name'],
                permission_codename=module_data['permission_codename']
            )

            # Create permission
            permission_name = f"Can access {module_data['name']} module"
            Permission.objects.create(
                codename=module_data['permission_codename'],
                name=permission_name,
                content_type=content_type,
            )

            self.stdout.write(f"Created module: {module.name} with permission: {module_data['permission_codename']}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded modules and permissions'))