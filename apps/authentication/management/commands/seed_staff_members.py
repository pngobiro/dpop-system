from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.organization.models import Role, Department, UserRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds staff members with their roles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding staff members...')

        # Define staff members with their details
        staff_members = [
            {
                'username': 'gilbert.kirui',
                'email': 'gilbert.kirui@judiciary.go.ke',
                'first_name': 'Gilbert',
                'last_name': 'Kirui',
                'role': 'Assistant Director',
                'is_staff': True
            },
            {
                'username': 'george.obai',
                'email': 'george.obai@judiciary.go.ke',
                'first_name': 'George',
                'last_name': 'Obai',
                'role': 'Assistant Director',
                'is_staff': True
            },
            {
                'username': 'dominic.nyambane',
                'email': 'dominic.nyambane@judiciary.go.ke',
                'first_name': 'Dominic',
                'last_name': 'Nyambane',
                'role': 'Assistant Director',
                'is_staff': True
            },
            # Programme Officers
            {
                'username': 'stanford.mwangi',
                'email': 'stanford.mwangi@judiciary.go.ke',
                'first_name': 'Stanford',
                'last_name': 'Mwangi',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'alex.njeru',
                'email': 'alex.njeru@judiciary.go.ke',
                'first_name': 'Alex',
                'last_name': 'Njeru',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'erick.kocheli',
                'email': 'erick.kocheli@judiciary.go.ke',
                'first_name': 'Erick',
                'last_name': 'Kocheli',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'steve.njehia',
                'email': 'steve.njehia@judiciary.go.ke',
                'first_name': 'Steve',
                'last_name': 'Njehia',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'eugene.omondi',
                'email': 'eugene.omondi@judiciary.go.ke',
                'first_name': 'Eugene',
                'last_name': 'Omondi',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'martin.astiba',
                'email': 'martin.astiba@judiciary.go.ke',
                'first_name': 'Martin',
                'last_name': 'Astiba',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'caroline.mungai',
                'email': 'caroline.mungai@judiciary.go.ke',
                'first_name': 'Caroline',
                'last_name': 'Mungai',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'linda.navakhole',
                'email': 'linda.navakhole@judiciary.go.ke',
                'first_name': 'Linda',
                'last_name': 'Navakhole',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'melly.kiprop',
                'email': 'melly.kiprop@judiciary.go.ke',
                'first_name': 'Melly',
                'last_name': 'Kiprop',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'john.mbiti',
                'email': 'john.mbiti@judiciary.go.ke',
                'first_name': 'John',
                'last_name': 'Mbiti',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'margaret.ochieng',
                'email': 'margaret.ochieng@judiciary.go.ke',
                'first_name': 'Margaret',
                'last_name': 'Ochieng',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'solomon.onaya',
                'email': 'solomon.onaya@judiciary.go.ke',
                'first_name': 'Solomon',
                'last_name': 'Onaya',
                'role': 'Programme Officer',
                'is_staff': True
            },
            {
                'username': 'yusuf.jarso',
                'email': 'yusuf.jarso@judiciary.go.ke',
                'first_name': 'Yusuf',
                'last_name': 'Jarso',
                'role': 'Programme Officer',
                'is_staff': True
            },
            # Office Assistants
            {
                'username': 'lucy.wangare',
                'email': 'lucy.wangare@judiciary.go.ke',
                'first_name': 'Lucy',
                'last_name': 'Wangare',
                'role': 'Office Assistant',
                'is_staff': True
            },
            {
                'username': 'hannah.gichuru',
                'email': 'hannah.gichuru@judiciary.go.ke',
                'first_name': 'Hannah',
                'last_name': 'Gichuru',
                'role': 'Office Assistant',
                'is_staff': True
            },
            {
                'username': 'lorna.barasa',
                'email': 'lorna.barasa@judiciary.go.ke',
                'first_name': 'Lorna',
                'last_name': 'Barasa',
                'role': 'Office Assistant',
                'is_staff': True
            },
        ]

        default_password = 'Staff@2024'

        # Get or create roles
        assistant_director_role, _ = Role.objects.get_or_create(name='Assistant Director')
        programme_officer_role, _ = Role.objects.get_or_create(name='Programme Officer')
        office_assistant_role, _ = Role.objects.get_or_create(name='Office Assistant')

        # Get department
        department = Department.objects.first()  # Assuming department exists
        if not department:
            self.stdout.write(self.style.ERROR('No department found. Please run seed_departments first.'))
            return

        # Create users and assign roles
        for staff_data in staff_members:
            # Create user if doesn't exist
            user, created = User.objects.get_or_create(
                username=staff_data['username'],
                defaults={
                    'email': staff_data['email'],
                    'first_name': staff_data['first_name'],
                    'last_name': staff_data['last_name'],
                    'is_staff': staff_data['is_staff']
                }
            )

            if created:
                user.set_password(default_password)
                user.save()
                # Add to department
                user.departments.add(department)

                # Assign role
                role = None
                if staff_data['role'] == 'Assistant Director':
                    role = assistant_director_role
                elif staff_data['role'] == 'Programme Officer':
                    role = programme_officer_role
                elif staff_data['role'] == 'Office Assistant':
                    role = office_assistant_role

                if role:
                    UserRole.objects.get_or_create(user=user, role=role)

                self.stdout.write(self.style.SUCCESS(f'Created user {user.username} with role {staff_data["role"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.username} already exists. Skipping.'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded staff members'))
        self.stdout.write('Default password for all users: Staff@2024')