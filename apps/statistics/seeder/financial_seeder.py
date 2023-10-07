# financial_seeder.py
from datetime import datetime
from apps.statistics.models import FinancialYear, FinancialQuarter

def run_financial_seeder():
    financial_years = [
        {'name': '2018/2019', 'start_date': '2018-07-01', 'end_date': '2019-06-30','id':1},
        {'name': '2019/2020', 'start_date': '2019-07-01', 'end_date': '2020-06-30','id':2},
        {'name': '2020/2021', 'start_date': '2020-07-01', 'end_date': '2021-06-30','id':3},
        {'name': '2021/2022', 'start_date': '2021-07-01', 'end_date': '2022-06-30','id':4},
        {'name': '2022/2023', 'start_date': '2022-07-01', 'end_date': '2023-06-30','id':5},
        {'name': '2023/2024', 'start_date': '2023-07-01', 'end_date': '2024-06-30','id':6},
        {'name': '2024/2025', 'start_date': '2024-07-01', 'end_date': '2025-06-30','id':7},
        {'name': '2025/2026', 'start_date': '2025-07-01', 'end_date': '2026-06-30','id':8},
        {'name': '2026/2027', 'start_date': '2026-07-01', 'end_date': '2027-06-30','id':9},
        {'name': '2027/2028', 'start_date': '2027-07-01', 'end_date': '2028-06-30','id':10},
        {'name': '2028/2029', 'start_date': '2028-07-01', 'end_date': '2029-06-30','id':11},
        {'name': '2029/2030', 'start_date': '2029-07-01', 'end_date': '2030-06-30','id':12},
        {'name': '2030/2031', 'start_date': '2030-07-01', 'end_date': '2031-06-30','id':13},
        # Add other financial year data here
    ]

    for fy_data in financial_years:
        financial_year = FinancialYear.objects.create(
            name=fy_data['name'],
            start_date=fy_data['start_date'],
            end_date=fy_data['end_date']
        )

        quarters = [
            {'name': 'Quarter 1', 'start_date': '07-01', 'end_date': '09-30'},
            {'name': 'Quarter 2', 'start_date': '10-01', 'end_date': '12-31'},
            {'name': 'Quarter 3', 'start_date': '01-01', 'end_date': '03-31'},
            {'name': 'Quarter 4', 'start_date': '04-01', 'end_date': '06-30'},
        ]

        for quarter_data in quarters:
            start_date = datetime.strptime(f'{financial_year.start_date.year}-{quarter_data["start_date"]}', '%Y-%m-%d').date()
            end_date = datetime.strptime(f'{financial_year.start_date.year}-{quarter_data["end_date"]}', '%Y-%m-%d').date()

            FinancialQuarter.objects.create(
                name=quarter_data['name'],
                start_date=start_date,
                end_date=end_date,
                financial_year=financial_year
            )

    print("Data seeding completed.")
