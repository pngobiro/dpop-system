from django.core.management.base import BaseCommand
from apps.statistics.models import Months

class Command(BaseCommand):
    help = 'Seed months data'

    def handle(self, *args, **options):
        months_data = [
            {'name': 'January', 'month_number': 31 ,"financial_quarter":3},
            {'name': 'February', 'month_number': 28 ,"financial_quarter":3},
            {'name': 'March', 'month_number': 31 ,"financial_quarter":3},
            {'name': 'April', 'month_number': 30,"financial_quarter":4},
            {'name': 'May', 'month_number': 31 ,"financial_quarter":4},
            {'name': 'June', 'month_number': 30 ,"financial_quarter":4},
            {'name': 'July', 'month_number': 31 ,"financial_quarter":1},
            {'name': 'August', 'month_number': 31 ,"financial_quarter":1},
            {'name': 'September', 'month_number': 30 ,"financial_quarter":1},
            {'name': 'October', 'month_number': 31 ,"financial_quarter":2},
            {'name': 'November', 'month_number': 30 ,"financial_quarter":2},
            {'name': 'December', 'month_number': 31 ,"financial_quarter":2},
        ]

        for month_data in months_data:
            Months.objects.create(
                name=month_data['name'],
                month_number=month_data['month_number'],
                financial_quarter=month_data['financial_quarter']
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded months data'))
