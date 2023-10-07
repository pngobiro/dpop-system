from django.core.management.base import BaseCommand
from apps.statistics.seeder import run_financial_seeder

class Command(BaseCommand):
    help = 'Seed financial data into the database.'

    def handle(self, *args, **options):
        run_financial_seeder()
        self.stdout.write(self.style.SUCCESS('Financial data seeded successfully.'))
