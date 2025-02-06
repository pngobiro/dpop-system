# apps/organization/management/commands/seed_organization.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.organization.models import Department, Role, UserRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds organization structure and users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating departments...')
        departments = {
            'directors_office': Department.objects.create(
                name="Director's Office",
                description="Office of the Director of Strategy, Planning and Organizational Performance"
            ),
            'performance': Department.objects.create(
                name="Performance Coordination",
                description="Performance monitoring and coordination"
            ),
            'planning': Department.objects.create(
                name="Planning, Monitoring & Evaluation",
                description="Planning, monitoring and evaluation activities"
            ),
            'research': Department.objects.create(
                name="Research & Statistics",
                description="Research and statistical analysis"
            ),
            'quality': Department.objects.create(
                name="Quality Assurance & Innovation",
                description="Quality assurance and innovation initiatives"
            )
        }

        self.stdout.write('Creating base roles...')
        base_roles = [
            ("Assistant Director", 'JSG3'),
            ("Court Assistant II", 'JSG4'),
            ("Economist I", 'JSG4'),
            ("Court Administrator I", 'JSG4'),
            ("Statistician II", 'JSG4'),
            ("Accountant I", 'JSG4'),
            ("Office Assistant I", 'JSG5'),
            ("Office Assistant II", 'JSG5'),
        ]

        roles = {}
        for dept in departments.values():
            for title, job_group in base_roles:
                role_key = f"{title}_{dept.name}".lower().replace(' ', '_').replace(',', '').replace('&', 'and')
                roles[role_key] = Role.objects.create(
                    title=title,
                    department=dept,
                    job_group=job_group
                )

        staff_data = [
            {'name': 'George Obai', 'pj': '64282', 'title': 'Assistant Director', 'dept': departments['performance']},
            {'name': 'Dominic Nyambane', 'pj': '64739', 'title': 'Assistant Director', 'dept': departments['planning']},
            {'name': 'Gilbert Kipkirui', 'pj': '69727', 'title': 'Assistant Director', 'dept': departments['research']},
            {'name': 'Victor Lumwamu', 'pj': '62751', 'title': 'Economist I', 'dept': departments['quality']},
            {'name': 'Alex Njeru', 'pj': '75665', 'title': 'Court Assistant II', 'dept': departments['planning']},
            {'name': 'Evelyne Simiyu', 'pj': '42505', 'title': 'Economist I', 'dept': departments['performance']},
            {'name': 'Linda Lukhale', 'pj': '44029', 'title': 'Court Administrator I', 'dept': departments['quality']},
            {'name': 'Martin Asitiba', 'pj': '33627', 'title': 'Court Assistant II', 'dept': departments['research']},
            {'name': 'Eric Kocheli', 'pj': '75681', 'title': 'Court Assistant II', 'dept': departments['research']},
            {'name': 'Solomon Onyara', 'pj': '76433', 'title': 'Court Assistant II', 'dept': departments['planning']},
            {'name': 'Caroline Mungai', 'pj': '75657', 'title': 'Court Assistant II', 'dept': departments['quality']},
            {'name': 'Margret Ochieng', 'pj': '80113', 'title': 'Court Assistant II', 'dept': departments['research']},
            {'name': 'Stanford Mwangi', 'pj': '47117', 'title': 'Court Assistant II', 'dept': departments['research']},
            {'name': 'Patrick Ngobiro', 'pj': '59433', 'title': 'Court Assistant II', 'dept': departments['directors_office']},
            {'name': 'John Mbiti', 'pj': '71530', 'title': 'Court Assistant II', 'dept': departments['performance']},
            {'name': 'Mercy Chemitai', 'pj': '71483', 'title': 'Court Assistant II', 'dept': departments['research']},
            {'name': 'Hannah Gichuki', 'pj': '54936', 'title': 'Office Assistant II', 'dept': departments['directors_office']},
            {'name': 'Lucy Gachoka', 'pj': '30982', 'title': 'Office Assistant I', 'dept': departments['directors_office']},
            {'name': 'Steve Njehia', 'pj': '57049', 'title': 'Accountant I', 'dept': departments['planning']},
            {'name': 'Leonard Melly', 'pj': '81485', 'title': 'Statistician II', 'dept': departments['research']},
            {'name': 'Lorna Barasa', 'pj': '82594', 'title': 'Office Assistant II', 'dept': departments['directors_office']}
        ]

        self.stdout.write('Creating staff users...')
        for staff in staff_data:
            user = User.objects.create(
                username=f"{staff['name'].lower().replace(' ', '.')}",
                first_name=staff['name'].split()[0],
                last_name=staff['name'].split()[-1],
                email=f"{staff['name'].lower().replace(' ', '.')}@judiciary.go.ke",
                pj_number=staff['pj']
            )
            user.set_password('Password123!')
            user.save()

            role_key = f"{staff['title']}_{staff['dept'].name}".lower().replace(' ', '_').replace(',', '').replace('&', 'and')
            role = roles[role_key]
            
            UserRole.objects.create(
                user=user,
                role=role,
                is_active=True
            )

        self.stdout.write('Creating director user...')
        director = User.objects.create(
            username='joseph.osewe',
            email='joseph.osewe@judiciary.go.ke',
            first_name='Joseph',
            last_name='Osewe',
            is_staff=True,
            is_superuser=True
        )
        director.set_password('Admin123!')
        director.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded organization data'))