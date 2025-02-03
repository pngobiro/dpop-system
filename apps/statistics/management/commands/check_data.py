# Create a new file: apps/statistics/management/commands/check_data.py

from django.core.management.base import BaseCommand
from apps.statistics.models import Unit, Division, UnitDivision

class Command(BaseCommand):
    help = 'Check existing data in database'

    def handle(self, *args, **options):
        self.stdout.write("Checking existing data...")
        
        self.stdout.write("\nDivisions:")
        for division in Division.objects.all():
            self.stdout.write(f"ID: {division.id}, Name: {division.name}")
            
        self.stdout.write("\nUnits:")
        for unit in Unit.objects.all():
            self.stdout.write(f"ID: {unit.id}, Name: {unit.name}")