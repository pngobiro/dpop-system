from django.core.management.base import BaseCommand

from apps.statistics.seeder.financial_seeder import seed_financial_periods

class Command(BaseCommand):
    help = 'Seed financial data into the database.'

    def handle(self, *args, **options):
        seed_financial_periods()
        self.stdout.write(self.style.SUCCESS('Financial data seeded successfully.'))
