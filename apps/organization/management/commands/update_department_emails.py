from django.core.management.base import BaseCommand
from apps.organization.models import Department

class Command(BaseCommand):
    help = 'Update department email addresses'

    def handle(self, *args, **options):
        self.stdout.write('Updating department emails...')
        
        department_emails = {
            "Director's Office": "directors.office@judiciary.go.ke",
            "Strategic planning and implementation Department": "strategic.planning@judiciary.go.ke",
            "Performance monitoring and evaluation Department": "monitoring.evaluation@judiciary.go.ke",
            "Research and data analytics Department": "research.analytics@judiciary.go.ke",
            "Quality assurance and innovation Department": "quality.assurance@judiciary.go.ke",
        }

        for dept_name, email in department_emails.items():
            try:
                dept = Department.objects.get(name=dept_name)
                dept.email = email
                dept.save()
                self.stdout.write(self.style.SUCCESS(f'  Updated {dept_name} with email: {email}'))
            except Department.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Department not found: {dept_name}'))

        self.stdout.write(self.style.SUCCESS('Successfully updated department emails'))