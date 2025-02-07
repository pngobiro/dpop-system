from datetime import datetime
from django.utils import timezone
from apps.statistics.models import FinancialYear, FinancialQuarter

def seed_financial_periods():
    """Seed financial years and quarters with proper date handling"""
    
    financial_years = [
        {'name': '2018/2019', 'start_date': '2018-07-01', 'end_date': '2019-06-30', 'id': 1},
        {'name': '2019/2020', 'start_date': '2019-07-01', 'end_date': '2020-06-30', 'id': 2},
        {'name': '2020/2021', 'start_date': '2020-07-01', 'end_date': '2021-06-30', 'id': 3},
        {'name': '2021/2022', 'start_date': '2021-07-01', 'end_date': '2022-06-30', 'id': 4},
        {'name': '2022/2023', 'start_date': '2022-07-01', 'end_date': '2023-06-30', 'id': 5},
        {'name': '2023/2024', 'start_date': '2023-07-01', 'end_date': '2024-06-30', 'id': 6},
        {'name': '2024/2025', 'start_date': '2024-07-01', 'end_date': '2025-06-30', 'id': 7},
        {'name': '2025/2026', 'start_date': '2025-07-01', 'end_date': '2026-06-30', 'id': 8},
    ]
    
    for fy_data in financial_years:
        # Create financial year with datetime objects
        financial_year = FinancialYear.objects.create(
            name=fy_data['name'],
            start_date=datetime.strptime(fy_data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(fy_data['end_date'], '%Y-%m-%d').date()
        )
        
        # Define quarters
        quarters = [
            {
                'name': 'Quarter 1',
                'start_date': f"{financial_year.start_date.year}-07-01",
                'end_date': f"{financial_year.start_date.year}-09-30",
                'quarter_number': 1
            },
            {
                'name': 'Quarter 2',
                'start_date': f"{financial_year.start_date.year}-10-01",
                'end_date': f"{financial_year.start_date.year}-12-31",
                'quarter_number': 2
            },
            {
                'name': 'Quarter 3',
                'start_date': f"{financial_year.end_date.year}-01-01",
                'end_date': f"{financial_year.end_date.year}-03-31",
                'quarter_number': 3
            },
            {
                'name': 'Quarter 4',
                'start_date': f"{financial_year.end_date.year}-04-01",
                'end_date': f"{financial_year.end_date.year}-06-30",
                'quarter_number': 4
            }
        ]
        
        # Create quarters with proper date handling
        for quarter_data in quarters:
            FinancialQuarter.objects.create(
                name=quarter_data['name'],
                start_date=datetime.strptime(quarter_data['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(quarter_data['end_date'], '%Y-%m-%d').date(),
                financial_year=financial_year,
                quarter_number=quarter_data['quarter_number']
            )
    
    print("Financial periods seeded successfully.")