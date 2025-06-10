import csv
from django.core.management.base import BaseCommand
from apps.statistics.models import Unit

class Command(BaseCommand):
    help = 'Populates the dcrt_unique_id field for each Unit using the court codes CSV.'

    def handle(self, *args, **options):
        # Create a mapping of court names to their IDs from the CSV
        court_mappings = {}
        csv_path = '/code/DCRT/DCRT COURT_CODES.csv'
        try:
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    court_name = row['court_name'].lower()
                    court_id = row['court_id']
                    court_mappings[court_name] = court_id

            # Update each unit's dcrt_unique_id if a match is found
            for unit in Unit.objects.all():
                unit_name = unit.name.lower()
                if unit_name in court_mappings:
                    unit.dcrt_unique_id = court_mappings[unit_name]
                    unit.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully updated dcrt_unique_id for {unit.name} to {unit.dcrt_unique_id}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'No matching court code found for {unit.name}'
                        )
                    )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    f'CSV file not found at {csv_path}. Please ensure the file exists in the correct location.'
                )
            )
            return