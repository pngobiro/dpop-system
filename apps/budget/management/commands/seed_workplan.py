# apps/budget/management/commands/seed_workplan.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.budget.models import (
    BudgetCategory, FinancialYear, WorkplanItem, 
    QuarterlyAllocation, PerformanceIndicator, TransformativeInitiative
)

class Command(BaseCommand):
    help = 'Seeds workplan data from financial workplan'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding workplan data...')

        # Create Financial Year
        fy, _ = FinancialYear.objects.get_or_create(
            name="2021/22",
            start_date="2021-07-01",
            end_date="2022-06-30"
        )

        # Create Budget Categories
        categories = {
            'leadership': BudgetCategory.objects.create(
                name="Transformative Leadership",
                code="TL"
            ),
            'governance': BudgetCategory.objects.create(
                name="Governance",
                code="GOV"
            ),
        }

        # Workplan Items
        workplan_data = [
            {
                'name': 'Regular Committee Conferences and Business',
                'budget_code': '2211002',
                'total_amount': 1900000,
                'item_type': 'regular',
                'category': categories['leadership'],
                'quarterly_allocation': {
                    1: 375000,
                    2: 375000,
                    3: 575000,
                    4: 575000
                },
                'performance_indicators': [
                    {
                        'name': '% of Statutory Documents',
                        'target': '100%',
                        'measurement_frequency': 'Quarterly'
                    }
                ]
            },
            {
                'name': 'Daily Subsistence Allowance',
                'budget_code': '2211003',
                'total_amount': 1600000,
                'item_type': 'regular',
                'category': categories['governance'],
                'quarterly_allocation': {
                    1: 400000,
                    2: 400000,
                    3: 400000,
                    4: 400000
                }
            },
            # Add more items from workplan...
        ]

        for item_data in workplan_data:
            # Create Workplan Item
            workplan_item = WorkplanItem.objects.create(
                name=item_data['name'],
                budget_code=item_data['budget_code'],
                total_amount=item_data['total_amount'],
                item_type=item_data['item_type'],
                category=item_data['category'],
                financial_year=fy
            )

            # Create Quarterly Allocations
            for quarter, amount in item_data['quarterly_allocation'].items():
                QuarterlyAllocation.objects.create(
                    workplan_item=workplan_item,
                    quarter=quarter,
                    amount=amount
                )

            # Create Performance Indicators if any
            if 'performance_indicators' in item_data:
                for indicator in item_data['performance_indicators']:
                    PerformanceIndicator.objects.create(
                        workplan_item=workplan_item,
                        name=indicator['name'],
                        target=indicator['target'],
                        measurement_frequency=indicator['measurement_frequency']
                    )

            # Create Transformative Initiative if applicable
            if item_data['item_type'] == 'transformative':
                TransformativeInitiative.objects.create(
                    workplan_item=workplan_item,
                    implementation_status='Not Started',
                    start_date=timezone.now(),
                    end_date=timezone.now() + timezone.timedelta(days=365)
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded workplan data'))