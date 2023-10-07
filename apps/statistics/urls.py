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

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id/months', views.rank_unit_division_months, name='unit_division_months'),
    
    path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/dcrt_summary', views.rank_unit_division_month_cases_summary, name='unit_division_month_cases_summary'),

    # upload unit_monthly_dcrt_excel

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/upload_dcrt', views.upload_unit_monthly_dcrt_excel, name='upload_unit_monthly_dcrt_excel'),


    # save excel data to db

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/save_dcrt', views.save_unit_monthly_dcrt_excel, name='save_unit_monthly_dcrt_excel'),


    # remove missing values from dataset

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/remove_missing_values', views.remove_missing_values, name='remove_missing_values'),

    # remove outliers from dataset

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/remove_outliers', views.remove_outliers, name='remove_outliers'),

    # view missing values

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/view_missing_values', views.view_missing_values, name='view_missing_values'),

    # view outliers

    path('rank/<int:id>/fy/<int:financial_year_id>/fq/<int:financial_quarter_id>/units/<int:unit_id>/division/<int:division_id>/months/<int:month_id>/cases/view_outliers', views.view_outliers, name='view_outliers'),


    
    
]
