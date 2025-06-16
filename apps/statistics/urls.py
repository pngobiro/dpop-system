# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.statistics.views.dashboard import home, rank_units
from apps.statistics.views.rank_unit_division_months import rank_unit_division_months
from apps.statistics.views.case_analysis import case_summary, monthly_unit_registered_cases, monthly_unit_resolved_cases
from apps.statistics.views.data_quality import monthly_unit_outliers, monthly_unit_missing_data, monthly_unit_duplicate_data, monthly_unit_incomplete_data
from apps.statistics.views.monthly_unit_matters_handled import monthly_unit_matters_handled
from apps.statistics.views.unit_division_quarters import unit_division_quarters
from apps.statistics.views.unit_division_fy import unit_division_fy
from apps.statistics.views.upload_unit_monthly_dcrt_excel import upload_unit_monthly_dcrt_excel
# Import for reports view will be added later

app_name = "statistics"

urlpatterns = [

    # The home page

    path('', home, name='home'),

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units', rank_units, name='rank_units'),

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/', rank_unit_division_months, name='unit_division_months'),
    
    # Reports URL pattern will be added back once the view is implemented

    # upload unit_monthly_dcrt_excel

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/upload_unit_monthly_dcrt_excel', upload_unit_monthly_dcrt_excel, name='upload_unit_monthly_dcrt_excel'),

    # case summary

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/case_summary', case_summary, name='monthly_unit_case_summary'),


    # remove missing values from dataset

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_outliers', monthly_unit_outliers, name='monthly_unit_outliers'),

    # remove outliers from dataset

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_missing_data', monthly_unit_missing_data, name='monthly_unit_missing_data'),

    # monthly_unit_duplicate_data

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_duplicate_data', monthly_unit_duplicate_data, name='monthly_unit_duplicate_data'),

    # view missing values

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_registered_cases', monthly_unit_registered_cases, name='monthly_unit_registered_cases'),

    # view outliers

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_resolved_cases', monthly_unit_resolved_cases, name='monthly_unit_resolved_cases'),

    # unit_division_quarters

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>', unit_division_quarters, name='unit_division_quarters'),


    # monthly_unit_matters_handled

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>', monthly_unit_matters_handled, name='monthly_unit_matters_handled'),

    #  monthly_unit_incomplete_data

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/incomplete_data', monthly_unit_incomplete_data, name='monthly_unit_incomplete_data'),


    # unit_division_fy

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>', unit_division_fy, name='unit_division_fy'),


    # monthly_unit_duplicate_data

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>', monthly_unit_duplicate_data, name='monthly_unit_duplicate_data'),
    
]
