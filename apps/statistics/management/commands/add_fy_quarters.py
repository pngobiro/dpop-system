import sys
from django.core.management.base import BaseCommand, CommandError
from apps.statistics.models import FinancialYear, FinancialQuarter
from datetime import date

class Command(BaseCommand):
        help = 'Adds the four standard financial quarters for a specified Financial Year.'

        def add_arguments(self, parser):
            parser.add_argument('fy_name', type=str, help='The name of the Financial Year (e.g., "2024/2025")')

        def handle(self, *args, **options):
            fy_name = options['fy_name']
            quarters_created_count = 0
            quarters_found_count = 0

            self.stdout.write(f"Attempting to add quarters for FY: {fy_name}")

            try:
                fy = FinancialYear.objects.get(name=fy_name)
                self.stdout.write(self.style.SUCCESS(f"Found Financial Year: {fy.name} (ID: {fy.id})"))

                quarters_data = [
                    {'number': 1, 'defaults': {'name': 'Q1', 'start_date': date(fy.start_date.year, 7, 1), 'end_date': date(fy.start_date.year, 9, 30)}},
                    {'number': 2, 'defaults': {'name': 'Q2', 'start_date': date(fy.start_date.year, 10, 1), 'end_date': date(fy.start_date.year, 12, 31)}},
                    {'number': 3, 'defaults': {'name': 'Q3', 'start_date': date(fy.end_date.year, 1, 1), 'end_date': date(fy.end_date.year, 3, 31)}},
                    {'number': 4, 'defaults': {'name': 'Q4', 'start_date': date(fy.end_date.year, 4, 1), 'end_date': date(fy.end_date.year, 6, 30)}},
                ]

                for q_data in quarters_data:
                    # Validate dates before creating
                    if q_data['defaults']['start_date'] > q_data['defaults']['end_date']:
                         self.stderr.write(self.style.ERROR(f"  Skipping Q{q_data['number']}: Start date {q_data['defaults']['start_date']} is after end date {q_data['defaults']['end_date']}."))
                         continue

                    try:
                        quarter, created = FinancialQuarter.objects.get_or_create(
                            financial_year=fy,
                            quarter_number=q_data['number'],
                            defaults=q_data['defaults']
                        )
                        if created:
                            quarters_created_count += 1
                            self.stdout.write(f"  Created Quarter: {quarter.name} ({quarter.start_date} - {quarter.end_date})")
                        else:
                            quarters_found_count += 1
                            self.stdout.write(f"  Found Quarter: {quarter.name} (already exists)")
                    except Exception as e_inner:
                         self.stderr.write(self.style.ERROR(f"  Error creating/getting Q{q_data['number']}: {e_inner}"))


                self.stdout.write(self.style.SUCCESS(f"\nSummary: Created {quarters_created_count} new quarters, Found {quarters_found_count} existing quarters for FY {fy_name}."))

            except FinancialYear.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Error: Financial Year '{fy_name}' not found."))
                sys.exit(1)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
                sys.exit(1)