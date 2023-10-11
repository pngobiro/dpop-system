from django.core.management.base import BaseCommand
from apps.statistics.models import Unit
import os
import csv

class Command(BaseCommand):
    help = 'Seed units from CSV file'

    def handle(self, *args, **options):
        Unit.objects.all().delete()  # Optional: Truncate the Unit table before seeding
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        with open(base_dir + '/data/unit.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                Unit.objects.create(
                    id=row[0],
                    name=row[1],
                    unique_id=row[2],
                    unique_code=row[3],
                    unit_rank_id=row[4],
                    head_id_fk=row[5],
                    subhead_id_fk=row[6],
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded units.'))


         