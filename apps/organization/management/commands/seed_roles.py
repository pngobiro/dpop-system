from django.core.management.base import BaseCommand
from apps.organization.models import Role, Department

class Command(BaseCommand):
    help = 'Seeds organization roles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding organization roles...')

        # Get Director's Office department
        directors_office = Department.objects.filter(name="Director's Office").first()
        if not directors_office:
            self.stdout.write(self.style.ERROR("Director's Office department not found"))
            return

        roles = [
            'Assistant Director',
            'Programme Officer',
            'Office Assistant'
        ]

        for role_title in roles:
            role, created = Role.objects.get_or_create(
                title=role_title,
                department=directors_office,
                defaults={
                    'description': f'{role_title} role in the organization',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created role: {role_title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Role already exists: {role_title}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded organization roles'))