from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tasks.models import Project, Task, Comment
from apps.organization.models import Department
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds sample projects and tasks'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding projects and tasks...')

        # Get or create a test user
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )

        # Get first department or None
        department = Department.objects.first()

        # Sample projects
        project_data = [
            {
                'name': 'Performance Management',
                'description': 'Implementing performance tracking system',
            },
            {
                'name': 'Document Digitization',
                'description': 'Converting physical documents to digital format',
            },
            {
                'name': 'Staff Training',
                'description': 'Organizing staff development programs',
            }
        ]

        for project_info in project_data:
            project, created = Project.objects.get_or_create(
                name=project_info['name'],
                defaults={
                    'description': project_info['description'],
                    'owner': user,
                    'department': department
                }
            )

            if created:
                self.stdout.write(f"Created project: {project.name}")

                # Create tasks for new projects
                tasks_data = [
                    {
                        'title': 'Initial Planning',
                        'status': Task.StatusChoices.DONE,
                        'priority': Task.PriorityChoices.HIGH,
                        'due_date': timezone.now().date()
                    },
                    {
                        'title': 'Implementation',
                        'status': Task.StatusChoices.IN_PROGRESS,
                        'priority': Task.PriorityChoices.MEDIUM,
                        'due_date': timezone.now().date()
                    },
                    {
                        'title': 'Review',
                        'status': Task.StatusChoices.TODO,
                        'priority': Task.PriorityChoices.LOW,
                        'due_date': timezone.now().date()
                    }
                ]

                for task_info in tasks_data:
                    task, task_created = Task.objects.get_or_create(
                        project=project,
                        title=f"{task_info['title']} - {project.name}",
                        defaults={
                            'description': f"Sample task for {project.name}",
                            'status': task_info['status'],
                            'priority': task_info['priority'],
                            'assignee': user,
                            'creator': user,
                            'due_date': task_info['due_date']
                        }
                    )
                    if task_created:
                        self.stdout.write(f"Created task: {task.title}")
            else:
                self.stdout.write(self.style.WARNING(f"Project '{project.name}' already exists. Skipping."))

        self.stdout.write(self.style.SUCCESS('Successfully seeded projects and tasks'))