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

    path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>', views.rank_units, name='rank_units'),




    # path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>/units/<int:unit_id>/months', views.rank_unit_months, name='rank_unit_months'),



    # path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>/units/<int:unit_id>/months/<int:month_id>', views.rank_unit_month, name='rank_unit_month'),

    
]
