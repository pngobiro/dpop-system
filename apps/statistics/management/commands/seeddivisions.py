import csv
from django.core.management.base import BaseCommand
from apps.statistics.models import Division
import os

class Command(BaseCommand):
    help = 'Seed divisions data'

    def handle(self, *args, **options):
        Division.objects.all().delete()
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        with open(base + '/data/division.csv') as csvfile:
            divisions_data = csv.reader(csvfile)
            next(divisions_data)  # Skip header row

            for data in divisions_data:
                Division.objects.create(
                    name=data[1],
                    is_active=bool(int(data[2])),
                    code=data[3],
                    deleted_at=None if data[4] == 'NULL' else data[4]
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded divisions data'))
