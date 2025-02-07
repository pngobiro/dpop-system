# apps/memos/management/commands/seed_memos.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.memos.models import Memo, MemoTemplate
from apps.organization.models import Department
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds sample memos data, making them visible to all users and departments.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding memos data...')

        departments = Department.objects.all()
        if not departments.exists():
            self.stdout.write(self.style.ERROR('No departments found. Run seed_organization first.'))
            return

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Run seed_organization first.'))
            return

        # --- Sample Data ---
        memo_subjects = [
            'Budget Allocation Update', 'Staff Meeting Schedule', 'Policy Changes Notification',
            'Training Program Announcement', 'Quarterly Performance Review', 'Office Closure Notice',
            'IT System Maintenance', 'Holiday Schedule', 'Project Timeline Update', 'Employee Wellness Program'
        ]
        memo_types = ['internal', 'external', 'circular']
        statuses = ['draft', 'pending_approval', 'approved', 'published', 'archived']  # Include 'published'

        # Get or create a default template.  It's good to have *at least* one.
        default_template, _ = MemoTemplate.objects.get_or_create(
            name="Default Template",
            defaults={
                'memo_type': 'internal',
                'description': 'A default memo template.',
                'content': 'This is a default memo template. Please replace this content.',
                'department': departments.first(),  # Associate with *a* department.
                'created_by': users.first(),       # Associate with *a* user.
                'is_active': True,
            }
        )

        # --- Create Memos ---
        for i in range(50):  # Create 50 sample memos
            creator = random.choice(users)
            department = random.choice(departments)  # The department *creating* the memo
            memo_type = random.choice(memo_types)
            status = random.choice(statuses)
            if status == 'published':
                published_at = timezone.now()
            else:
                published_at = None

            memo = Memo.objects.create(
                title=random.choice(memo_subjects),
                reference_number=f"MEMO/{fake.unique.random_number(digits=6)}/{timezone.now().year}",
                memo_type=memo_type,
                template=default_template,  # Use the default template
                content=fake.paragraph(nb_sentences=5),
                department=department,  # Department *creating* the memo
                status=status,
                created_by=creator,
                is_confidential=random.choice([True, False]),
                file_number=f"FILE/{fake.unique.random_number(digits=4)}/{timezone.now().year}",
                tags=','.join(fake.words(nb=3)),
                version_number=1,
                published_at = published_at
            )
            # --- Permissions (Two Approaches) ---

            # Approach 1: Add all departments as recipients (Easiest)
            memo.recipient_departments.set(departments)  # Add *all* departments
            memo.recipient_users.set(users)          # Add *all* users

            # Approach 2: (More Granular, using Permissions - Requires more setup)
            #   - You would need to create a custom permission (e.g., 'view_all_memos') in your
            #     `apps/memos/models.py` (Meta.permissions).
            #   - Then, in your seed_organization command, grant this permission to all users.
            #   - Here, you would check:  if request.user.has_perm('memos.view_all_memos'): ...

            self.stdout.write(self.style.SUCCESS(f'Created memo: {memo.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded memos data'))