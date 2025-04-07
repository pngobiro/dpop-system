from django.core.management.base import BaseCommand
from apps.organization.models import Department

class Command(BaseCommand):
    help = 'Seeds the database with initial departments'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Departments...')

        departments_to_create = [
            {"name": "Director's Office", "description": "Office of the Director"},
            {"name": "Strategic planning and implementation Department", "description": ""},
            {"name": "Performance monitoring and evaluation Department", "description": ""},
            {"name": "Research and data analytics Department", "description": ""},
            {"name": "Quality assurance and innovation Department", "description": ""},
        ]

        created_count = 0
        for dept_data in departments_to_create:
            department, created = Department.objects.get_or_create(
                name=dept_data["name"],
                defaults={'description': dept_data["description"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Department: {department.name}'))
                created_count += 1
            else:
                self.stdout.write(f'  Department already exists: {department.name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} new Departments.'))