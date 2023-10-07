# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.statistics import views
from django.urls import path, include

urlpatterns = [

    # The home page

    path('', views.home, name='home'),
    # path ro rank with id , financial year id and financial quarter id
    path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>', views.rank, name='rank_fy_fq'),

    # path to a rank with id and financial year id , financial quarter id and financial and list of units of the rank

    path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>/units', views.rank_units, name='rank_units'),

    # path to a rank with id and financial year id , financial quarter id and financial , unit id and list of months.

    path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>/units/<int:unit_id>/months', views.rank_unit_months, name='rank_unit_months'),

    # path to a rank with id and financial year id , financial quarter id and financial , unit id and month id.

    path('rank/<int:id>/<int:financial_year_id>/<int:financial_quarter_id>/units/<int:unit_id>/months/<int:month_id>', views.rank_unit_month, name='rank_unit_month'),

    
]
