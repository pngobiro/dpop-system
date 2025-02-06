# apps/memos/management/commands/seed_memos.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.memos.models import Memo, MemoTemplate, MemoApproval
from apps.organization.models import Department
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds sample memos data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding memos data...')

        # Get or create departments if they don't exist
        departments = Department.objects.all()
        if not departments.exists():
            self.stdout.write('No departments found. Please run seed_organization first.')
            return

        # Get users or create some if they don't exist
        users = User.objects.all()
        if not users.exists():
            self.stdout.write('No users found. Please run seed_organization first.')
            return

        # Create memo templates
        template_types = [
            ('Internal Memo Template', 'internal', 'Standard template for internal communications'),
            ('External Letter Template', 'external', 'Template for external correspondence'),
            ('Circular Template', 'circular', 'Template for departmental circulars')
        ]

        for name, memo_type, desc in template_types:
            for dept in departments:
                MemoTemplate.objects.get_or_create(
                    name=f"{name} - {dept.name}",
                    defaults={
                        'memo_type': memo_type,
                        'description': desc,
                        'content': fake.text(max_nb_chars=500),
                        'department': dept,
                        'created_by': random.choice(users)
                    }
                )

        # Create sample memos
        memo_subjects = [
            'Budget Allocation Update',
            'Staff Meeting Schedule',
            'Policy Changes Notification',
            'Training Program Announcement',
            'Quarterly Performance Review',
            'Office Closure Notice',
            'IT System Maintenance',
            'Holiday Schedule',
            'Project Timeline Update',
            'Employee Wellness Program'
        ]

        statuses = ['draft', 'pending_approval', 'approved', 'published', 'archived']
        
        # Create 50 sample memos
        for _ in range(50):
            department = random.choice(departments)
            creator = random.choice(users)
            memo_type = random.choice(['internal', 'external', 'circular'])
            status = random.choice(statuses)

            memo = Memo.objects.create(
                title=random.choice(memo_subjects),
                reference_number=f"MEMO/{fake.unique.random_number(digits=6)}/{timezone.now().year}",
                memo_type=memo_type,
                content=fake.text(max_nb_chars=1000),
                department=department,
                status=status,
                created_by=creator,
                is_confidential=random.choice([True, False]),
                file_number=f"FILE/{fake.unique.random_number(digits=4)}/{timezone.now().year}",
                tags=','.join(fake.words(3)),
                version_number=1
            )

            # Add recipients
            memo.recipient_departments.add(*random.sample(list(departments), k=random.randint(1, 3)))
            memo.recipient_users.add(*random.sample(list(users), k=random.randint(2, 5)))

            # Create approval workflow if memo is pending or approved
            if status in ['pending_approval', 'approved']:
                approvers = random.sample(list(users), k=random.randint(2, 4))
                for level, approver in enumerate(approvers, 1):
                    MemoApproval.objects.create(
                        memo=memo,
                        approver=approver,
                        status='approved' if status == 'approved' else 'pending',
                        level=level,
                        comments=fake.text(max_nb_chars=100) if status == 'approved' else ''
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded memos data'))