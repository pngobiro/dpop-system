# apps/innovations/management/commands/seed_innovations.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.innovations.models import Innovation, InnovationAttachment
from apps.statistics.models import Unit, FinancialYear
from faker import Faker
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the Innovation model with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Innovation data...')

        # --- Prerequisites ---
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Run seed_organization first.'))
            return

        units = Unit.objects.all()
        if not units.exists():
            self.stdout.write(self.style.ERROR('No units found. Run seed_statistics first.'))
            return

        financial_years = FinancialYear.objects.all()
        if not financial_years.exists():
            self.stdout.write(self.style.ERROR('No financial years found. Run seed_organization first.'))
            return

        # --- Sample Data ---
        fake = Faker()
        categories = [
            'efficiency', 'vulnerable', 'security', 'access', 'partnerships',
            'mentorship', 'financial', 'employee', 'environment', 'other'
        ]
        statuses = ['innovation', 'best_practice', 'rejected']

        # --- Create Innovations ---
        for _ in range(30):  # Create 30 innovations
            submitted_by = random.choice(users)
            court = random.choice(units)
            financial_year = random.choice(financial_years)
            is_replication = random.choice([True, False])
            source_court = fake.company() if is_replication else None
            category = random.choice(categories)
            status = random.choice(statuses) #random choice of the status
            approved_by = random.choice(users) if status == 'best_practice' else None #approved by a random user

            innovation = Innovation.objects.create(
                court=court,
                station=fake.city(),
                financial_year=financial_year,
                title=fake.catch_phrase(),
                is_replication=is_replication,
                source_court=source_court,
                category=category,
                situation_before=fake.paragraph(nb_sentences=3),
                description=fake.paragraph(nb_sentences=5),
                solution=fake.paragraph(nb_sentences=5),
                replication_potential=fake.paragraph(nb_sentences=2),
                individuals_involved=', '.join([fake.name() for _ in range(random.randint(1, 5))]),
                stakeholders_affected=', '.join([fake.word() for _ in range(random.randint(1, 3))]),
                status=status,
                submitted_by=submitted_by,
                approved_by = approved_by # assigned approved by
            )
            # create attachments
            for _ in range(random.randint(0, 3)):  # 0-3 attachments
                try:
                    InnovationAttachment.objects.create(
                        innovation=innovation,
                        file=f"dummy_file_{random.randint(1,100)}.txt",  # Dummy filename, as we're not really uploading.
                        uploaded_by=submitted_by,
                )
                except Exception as e:
                    print(e)
                    continue

            self.stdout.write(self.style.SUCCESS(f'Created innovation: {innovation.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded Innovation data'))