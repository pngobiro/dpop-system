import csv
from django.core.management.base import BaseCommand
import os 
from apps.statistics.models import UnitDivision

class Command(BaseCommand):
    help = 'Seed Unit Division data from CSV file'

    def handle(self, *args, **options):
        # id , unit_id , division_id .

        UnitDivision.objects.all().delete()  # Optional: Truncate the UnitDivision table before seeding

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        with open(base_dir + '/data/unit_division.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                UnitDivision.objects.create(
                    id=row[0],
                    unit_id=row[1],
                    division_id=row[2],
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Unit Division.'))