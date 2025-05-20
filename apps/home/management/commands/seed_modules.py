from django.core.management.base import BaseCommand
from apps.home.models import Module

class Command(BaseCommand):
    help = 'Seeds modules for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding modules...')

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
                'name': 'Tasks',
                'description': 'Manage tasks and track progress',
                'icon_class': 'fas fa-tasks',
                'url_name': 'tasks:dashboard',
                'permission_codename': 'access_tasks'
            },
            {
                'name': 'Reports',
                'description': 'Generate and download reports',
                'icon_class': 'fas fa-file-pdf',
                'url_name': 'reports:dashboard',
                'permission_codename': 'access_reports'
            },
            {
                'name': 'Mail',
                'description': 'Manage physical mail',
                'icon_class': 'fas fa-envelope',
                'url_name': 'mail:physical_list',
                'permission_codename': 'access_mail'
            },
            {
                'name': 'Surveys',
                'description': 'Create and manage surveys',
                'icon_class': 'fas fa-poll',
                'url_name': 'surveys:dashboard',
                'permission_codename': 'access_surveys'
            },
            {
                'name': 'PMMU Evaluation',
                'description': 'PMMU Evaluation and Target Setting',
                'icon_class': 'fas fa-chart-line',
                'url_name': 'pmmu_evaluation:dashboard',
                'permission_codename': 'access_pmmu_evaluation'
            },
            {
                'name': 'Innovations',
                'description': 'Innovations and Best Practices',
                'icon_class': 'fas fa-lightbulb',
                'url_name': 'innovations:dashboard',
                'permission_codename': 'access_innovations'
            }
        ]

        for module_data in modules_data:
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

        self.stdout.write(self.style.SUCCESS('Successfully seeded modules'))
