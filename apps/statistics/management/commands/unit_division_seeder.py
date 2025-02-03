from django.core.management.base import BaseCommand
import os
import csv
from apps.statistics.models import UnitDivision, Unit, Division

class Command(BaseCommand):
    help = 'Seed Unit Division data from CSV file'

    def handle(self, *args, **options):
        self.stdout.write("Starting Unit Division seeding...")
        
        # Clear existing data
        UnitDivision.objects.all().delete()
        self.stdout.write("Cleared existing Unit Division data")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        success_count = 0
        error_count = 0
        skipped_count = 0
        
        with open(base_dir + '/data/unit_division.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                try:
                    unit_id = int(row[1])
                    division_id = int(row[2])
                    
                    # Check if Unit exists and can have divisions
                    try:
                        unit = Unit.objects.get(id=unit_id)
                        
                        # Skip if unit cannot have divisions
                        if not unit.has_division:
                            self.stdout.write(f'Skipping unit {unit.name} (ID: {unit_id}) - Cannot have divisions')
                            skipped_count += 1
                            continue
                            
                        division = Division.objects.get(id=division_id)
                        
                        # Create UnitDivision
                        UnitDivision.objects.create(
                            id=int(row[0]),
                            unit=unit,
                            division=division,
                        )
                        success_count += 1
                        
                    except Unit.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Unit with id {unit_id} does not exist'))
                        error_count += 1
                    except Division.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Division with id {division_id} does not exist'))
                        error_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error processing row {row}: {str(e)}'))
                        error_count += 1
                        
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f'Invalid data in row {row}: {str(e)}'))
                    error_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Finished seeding Unit Divisions.\n'
            f'Successfully processed: {success_count} records\n'
            f'Skipped (no divisions allowed): {skipped_count} records\n'
            f'Errors encountered: {error_count} records'
        ))