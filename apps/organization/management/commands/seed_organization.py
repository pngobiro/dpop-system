# apps/organization/management/commands/seed_organization.py
from django.core.management.base import BaseCommand
from apps.organization.models import Department, Role

class Command(BaseCommand):
    help = 'Seeds basic organizational structure'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding organization data...')

        # Create Departments
        departments_data = [
            {
                'name': "Director's Office",
                'description': "Overall leadership of strategy development, planning, research, performance improvement, and innovation"
            },
            {
                'name': "Organizational Productivity & Quality Assurance",
                'description': "Focuses on workflow optimization, performance standards, and quality management"
            },
            {
                'name': "Planning, Monitoring & Evaluation",
                'description': "Handles strategic planning, implementation, monitoring, and evaluation"
            },
            {
                'name': "Research & Data Analytics",
                'description': "Drives evidence-based decision making and manages judicial data and research"
            }
        ]

        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            departments[dept_data['name']] = dept
            if created:
                self.stdout.write(f'Created department: {dept.name}')

        # Create Roles
        roles_data = [
            # Director's Office
            {
                'department': "Director's Office",
                'title': "Director of Strategy, Planning and Organizational Productivity",
                'job_group': 'JSG1',
                'description': "Overall leadership and reporting to top judiciary leadership"
            },
            # Organizational Productivity & QA
            {
                'department': "Organizational Productivity & Quality Assurance",
                'title': "Deputy Director - Organizational Productivity & QA",
                'job_group': 'JSG2',
                'description': "Leads workflow optimization and quality management"
            },
            {
                'department': "Organizational Productivity & Quality Assurance",
                'title': "Assistant Director - Organizational Productivity",
                'job_group': 'JSG3',
                'description': "Manages organizational productivity initiatives"
            },
            {
                'department': "Organizational Productivity & Quality Assurance",
                'title': "Assistant Director - Quality Assurance & Innovation",
                'job_group': 'JSG3',
                'description': "Manages quality assurance and innovation programs"
            },
            # Planning, M&E
            {
                'department': "Planning, Monitoring & Evaluation",
                'title': "Deputy Director - Planning, M&E",
                'job_group': 'JSG2',
                'description': "Leads strategic planning and evaluation"
            },
            {
                'department': "Planning, Monitoring & Evaluation",
                'title': "Assistant Director - Strategy and Planning",
                'job_group': 'JSG3',
                'description': "Manages strategic planning implementation"
            },
            # Research & Data Analytics
            {
                'department': "Research & Data Analytics",
                'title': "Deputy Director - Research & Data Analytics",
                'job_group': 'JSG2',
                'description': "Leads research and data analytics initiatives"
            },
            {
                'department': "Research & Data Analytics",
                'title': "Assistant Director - Data Analytics",
                'job_group': 'JSG3',
                'description': "Manages data analytics operations"
            },
            {
                'department': "Research & Data Analytics",
                'title': "Research Officer",
                'job_group': 'JSG4',
                'description': "Conducts research and analysis"
            }
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                title=role_data['title'],
                department=departments[role_data['department']],
                defaults={
                    'job_group': role_data['job_group'],
                    'description': role_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created role: {role.title}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded organization data'))