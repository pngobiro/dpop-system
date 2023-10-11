# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.statistics import views

app_name = "apps.statistics"

urlpatterns = [

    # The home page

    path('', views.home, name='home'),

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units', views.rank_units, name='rank_units'),

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months', views.rank_unit_division_months, name='unit_division_months'),
    
    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/dcrt_summary', views.rank_unit_division_month_cases_summary, name='unit_division_month_cases_summary'),

    # upload unit_monthly_dcrt_excel

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/upload_unit_monthly_dcrt_excel', views.upload_unit_monthly_dcrt_excel, name='upload_unit_monthly_dcrt_excel'),

    # case summary

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/case_summary', views.case_summary, name='monthly_unit_case_summary'),


    # remove missing values from dataset

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_outliers', views.monthly_unit_outliers, name='monthly_unit_outliers'),

    # remove outliers from dataset

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_missing_data', views.monthly_unit_missing_data, name='monthly_unit_missing_data'),

    # monthly_unit_duplicate_data

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_duplicate_data', views.monthly_unit_duplicate_data, name='monthly_unit_duplicate_data'),

    # view missing values

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_registered_cases', views.monthly_unit_registered_cases, name='monthly_unit_registered_cases'),

    # view outliers

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/monthly_unit_resolved_cases', views.monthly_unit_resolved_cases, name='monthly_unit_resolved_cases'),

    # unit_division_quarters

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>', views.unit_division_quarters, name='unit_division_quarters'),


    # monthly_unit_matters_handled

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>', views.monthly_unit_matters_handled, name='monthly_unit_matters_handled'),

    #  monthly_unit_incomplete_data

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/incomplete_data', views.monthly_unit_incomplete_data, name='monthly_unit_incomplete_data'),


    # unit_division_fy

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>', views.unit_division_fy, name='unit_division_fy'),


    # monthly_unit_duplicate_data

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>', views.monthly_unit_duplicate_data, name='monthly_unit_duplicate_data'),
    
]
