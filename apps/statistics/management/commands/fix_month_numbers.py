from django.core.management.base import BaseCommand
from apps.statistics.models import Months

class Command(BaseCommand):
    help = 'Corrects the month_number field in the Months table to be 1-12 instead of days.'

    def handle(self, *args, **options):
        updates = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 
            'May': 5, 'June': 6, 'July': 7, 'August': 8, 
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        total_updated = 0
        
        self.stdout.write("Starting update of month_number field...")
        
        for name, num in updates.items():
            try:
                updated_rows = Months.objects.filter(name__iexact=name).update(month_number=num)
                if updated_rows > 0:
                    self.stdout.write(self.style.SUCCESS(f"  Updated {name} to month_number {num} ({updated_rows} record(s))"))
                    total_updated += updated_rows
                else:
                     self.stdout.write(f"  No records found or needed update for {name}.")
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  Error updating {name}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nFinished. Total records updated: {total_updated}"))