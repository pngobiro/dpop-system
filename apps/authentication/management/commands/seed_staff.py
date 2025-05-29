from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.organization.models import Role, Department, UserRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds staff users if none exist'

    def handle(self, *args, **kwargs):
        default_password = 'Staff@2024'
        
        # Get roles
        assistant_director_role = Role.objects.get(title='Assistant Director')
        programme_officer_role = Role.objects.get(title='Programme Officer')
        office_assistant_role = Role.objects.get(title='Office Assistant')

        # Get department
        department = Department.objects.first()
        if not department:
            self.stdout.write(self.style.ERROR('No department found. Please run seed_departments first.'))
            return

        # Define staff members
        staff_members = [
            # Assistant Directors
            {
                'username': 'gilbert.kirui',
                'email': 'gilbert.kirui@judiciary.go.ke',
                'first_name': 'Gilbert',
                'last_name': 'Kirui',
                'role': assistant_director_role
            },
            {
                'username': 'george.obai',
                'email': 'george.obai@judiciary.go.ke',
                'first_name': 'George',
                'last_name': 'Obai',
                'role': assistant_director_role
            },
            {
                'username': 'dominic.nyambane',
                'email': 'dominic.nyambane@judiciary.go.ke',
                'first_name': 'Dominic',
                'last_name': 'Nyambane',
                'role': assistant_director_role
            },
            # Programme Officers
            {
                'username': 'stanford.mwangi',
                'email': 'stanford.mwangi@judiciary.go.ke',
                'first_name': 'Stanford',
                'last_name': 'Mwangi',
                'role': programme_officer_role
            },
            {
                'username': 'alex.njeru',
                'email': 'alex.njeru@judiciary.go.ke',
                'first_name': 'Alex',
                'last_name': 'Njeru',
                'role': programme_officer_role
            },
            {
                'username': 'erick.kocheli',
                'email': 'erick.kocheli@judiciary.go.ke',
                'first_name': 'Erick',
                'last_name': 'Kocheli',
                'role': programme_officer_role
            },
            {
                'username': 'steve.njehia',
                'email': 'steve.njehia@judiciary.go.ke',
                'first_name': 'Steve',
                'last_name': 'Njehia',
                'role': programme_officer_role
            },
            {
                'username': 'eugene.omondi',
                'email': 'eugene.omondi@judiciary.go.ke',
                'first_name': 'Eugene',
                'last_name': 'Omondi',
                'role': programme_officer_role
            },
            {
                'username': 'martin.astiba',
                'email': 'martin.astiba@judiciary.go.ke',
                'first_name': 'Martin',
                'last_name': 'Astiba',
                'role': programme_officer_role
            },
            {
                'username': 'caroline.mungai',
                'email': 'caroline.mungai@judiciary.go.ke',
                'first_name': 'Caroline',
                'last_name': 'Mungai',
                'role': programme_officer_role
            },
            {
                'username': 'linda.navakhole',
                'email': 'linda.navakhole@judiciary.go.ke',
                'first_name': 'Linda',
                'last_name': 'Navakhole',
                'role': programme_officer_role
            },
            {
                'username': 'melly.kiprop',
                'email': 'melly.kiprop@judiciary.go.ke',
                'first_name': 'Melly',
                'last_name': 'Kiprop',
                'role': programme_officer_role
            },
            {
                'username': 'john.mbiti',
                'email': 'john.mbiti@judiciary.go.ke',
                'first_name': 'John',
                'last_name': 'Mbiti',
                'role': programme_officer_role
            },
            {
                'username': 'margaret.ochieng',
                'email': 'margaret.ochieng@judiciary.go.ke',
                'first_name': 'Margaret',
                'last_name': 'Ochieng',
                'role': programme_officer_role
            },
            {
                'username': 'solomon.onaya',
                'email': 'solomon.onaya@judiciary.go.ke',
                'first_name': 'Solomon',
                'last_name': 'Onaya',
                'role': programme_officer_role
            },
            {
                'username': 'yusuf.jarso',
                'email': 'yusuf.jarso@judiciary.go.ke',
                'first_name': 'Yusuf',
                'last_name': 'Jarso',
                'role': programme_officer_role
            },
            # Office Assistants
            {
                'username': 'lucy.wangare',
                'email': 'lucy.wangare@judiciary.go.ke',
                'first_name': 'Lucy',
                'last_name': 'Wangare',
                'role': office_assistant_role
            },
            {
                'username': 'hannah.gichuru',
                'email': 'hannah.gichuru@judiciary.go.ke',
                'first_name': 'Hannah',
                'last_name': 'Gichuru',
                'role': office_assistant_role
            },
            {
                'username': 'lorna.barasa',
                'email': 'lorna.barasa@judiciary.go.ke',
                'first_name': 'Lorna',
                'last_name': 'Barasa',
                'role': office_assistant_role
            },
        ]

        for staff_data in staff_members:
            user, created = User.objects.get_or_create(
                username=staff_data['username'],
                defaults={
                    'email': staff_data['email'],
                    'first_name': staff_data['first_name'],
                    'last_name': staff_data['last_name'],
                    'is_staff': True
                }
            )

            if created:
                user.set_password(default_password)
                user.save()
                # Add to department
                user.departments.add(department)

                # Assign role
                UserRole.objects.get_or_create(user=user, role=staff_data['role'])
                self.stdout.write(self.style.SUCCESS(f'Created user {user.username} with role {staff_data["role"].title}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.username} already exists. Skipping.'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded all staff members'))
        self.stdout.write('Default password for all users: Staff@2024')