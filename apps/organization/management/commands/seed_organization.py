# apps/organization/management/commands/seed_organization.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.organization.models import Department, Role, UserRole
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.home.models import Module
from apps.statistics.models import FinancialYear, FinancialQuarter # Import
from datetime import datetime
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds organization structure, users, roles, and permissions'

    def handle(self, *args, **kwargs):

        # --- Clear Existing Data ---
        self.stdout.write('Clearing existing organization data...')
        UserRole.objects.all().delete()
        Role.objects.all().delete()
        Department.objects.all().delete()
        User.objects.all().delete()  # Be *very* careful with this in production!

        # --- Departments ---
        self.stdout.write('Creating departments...')
        departments = {
            'directors_office': Department.objects.create(
                name="Director's Office",
                description="Office of the Director of Strategy, Planning and Organizational Performance",
                is_active=True
            ),
            'performance': Department.objects.create(
                name="Performance Coordination",
                description="Performance monitoring and coordination",
                is_active=True
            ),
            'planning': Department.objects.create(
                name="Planning, Monitoring & Evaluation",
                description="Planning, monitoring and evaluation activities",
                is_active=True
            ),
            'research': Department.objects.create(
                name="Research & Statistics",
                description="Research and statistical analysis",
                is_active=True
            ),
            'quality': Department.objects.create(
                name="Quality Assurance & Innovation",
                description="Quality assurance and innovation initiatives",
                is_active=True
            )
        }

        # --- Roles ---
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

        # --- Staff Data ---
        staff_data = [
            # ... (Your existing staff data - as before) ...
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
            username = staff['name'].lower().replace(' ', '.')
            email = f"{username}@judiciary.go.ke"
            first_name = staff['name'].split()[0]
            last_name = ' '.join(staff['name'].split()[1:])  # Handle multi-part last names
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'pj_number': staff['pj'],
                    'is_staff': True,  # Important: Mark users as staff
                }
            )
            if created:
                user.set_password('Password123!')  # ALWAYS set a password
                user.save()


            role_key = f"{staff['title']}_{staff['dept'].name}".lower().replace(' ', '_').replace(',', '').replace('&', 'and')

            #CRITICAL FIX: Check if the role exists!
            if role_key in roles:
                role = roles[role_key]
                # Associate user with department directly.
                user.departments.add(staff['dept']) #add the department to the user
                user.save()

                user_role = UserRole.objects.create(
                    user=user,
                    role=role,
                    is_active=True
                 )
                # --- Grant Permissions ---
                # Get all content types for the apps you want to manage
                content_types = ContentType.objects.filter(
                    app_label__in=['budget', 'document_management', 'meetings', 'memos', 'mail', 'statistics']  # Add your app labels here
                )

                # Get all permissions for those content types
                permissions = Permission.objects.filter(content_type__in=content_types)

                # Assign permissions based on role (Example)
                if role.title == "Assistant Director":
                    # Grant all permissions to Assistant Directors
                    role.permissions.set(permissions) # important, use .set()
                elif role.title.startswith("Court Assistant"):
                    # Grant view permissions to Court Assistants.  This is a very basic example.
                    for perm in permissions:
                        if 'view' in perm.codename:
                            role.permissions.add(perm)
            else:
                self.stdout.write(self.style.ERROR(f"Role key '{role_key}' not found!"))


        self.stdout.write('Creating director user...')
        director, created = User.objects.get_or_create(
            username='joseph.osewe',
            defaults={
                'email': 'joseph.osewe@judiciary.go.ke',
                'first_name': 'Joseph',
                'last_name': 'Osewe',
                'is_staff': True,
                'is_superuser': True  # Correctly sets superuser status
            }
        )
        if created:
            director.set_password('Admin123!')
            director.save()
        director.departments.add(departments['directors_office']) # Assign director to a dept.
        director_role_key = f"assistant_director_{departments['directors_office'].name}".lower()

        if director_role_key in roles:
             director_role = roles[director_role_key]
             UserRole.objects.create(user = director, role = director_role, is_active = True)
             # --- Grant Permissions to Director---
             module_content_type = ContentType.objects.get_for_model(Module)
             module_permissions = Permission.objects.filter(content_type=module_content_type)
             for perm in module_permissions:
                director_role.permissions.add(perm)
        # --- Seed Financial Data ---
        self.seed_financial_periods()
        self.stdout.write(self.style.SUCCESS('Successfully seeded organization data'))

    def seed_financial_periods(self):
        financial_years = [
            {'name': '2018/2019', 'start_date': '2018-07-01', 'end_date': '2019-06-30'},
            {'name': '2019/2020', 'start_date': '2019-07-01', 'end_date': '2020-06-30'},
            {'name': '2020/2021', 'start_date': '2020-07-01', 'end_date': '2021-06-30'},
            {'name': '2021/2022', 'start_date': '2021-07-01', 'end_date': '2022-06-30'},
             {'name': '2022/2023', 'start_date': '2022-07-01', 'end_date': '2023-06-30'},
            {'name': '2023/2024', 'start_date': '2023-07-01', 'end_date': '2024-06-30'},
        ]

        for fy_data in financial_years:
            financial_year, created = FinancialYear.objects.get_or_create(
                name=fy_data['name'],
                defaults={
                    'start_date': timezone.make_aware(datetime.strptime(fy_data['start_date'], '%Y-%m-%d')),
                    'end_date': timezone.make_aware(datetime.strptime(fy_data['end_date'], '%Y-%m-%d')),
                }
            )
            if created:
              self.stdout.write(f'Created financial year: {financial_year.name}')


            quarters = [
                {'name': 'Quarter 1', 'start_date': '07-01', 'end_date': '09-30', 'quarter_number': 1},
                {'name': 'Quarter 2', 'start_date': '10-01', 'end_date': '12-31', 'quarter_number': 2},
                {'name': 'Quarter 3', 'start_date': '01-01', 'end_date': '03-31', 'quarter_number': 3},
                {'name': 'Quarter 4', 'start_date': '04-01', 'end_date': '06-30', 'quarter_number': 4},
            ]

            for quarter_data in quarters:
                start_date = timezone.make_aware(datetime.strptime(f"{financial_year.start_date.year}-{quarter_data['start_date']}", '%Y-%m-%d'))
                # Handle year rollover for Q3 and Q4
                end_year = financial_year.end_date.year
                end_date = timezone.make_aware(datetime.strptime(f"{end_year}-{quarter_data['end_date']}", '%Y-%m-%d'))

                quarter, created = FinancialQuarter.objects.get_or_create(
                    financial_year=financial_year,
                    quarter_number=quarter_data['quarter_number'],
                    defaults={
                        'name': quarter_data['name'],
                        'start_date': start_date,
                        'end_date': end_date,
                    }

                )
                if created:
                     self.stdout.write(f'Created quarter: {quarter.name}')