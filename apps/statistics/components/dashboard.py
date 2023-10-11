# views.py
from django_unicorn.components import UnicornView
from django.shortcuts import redirect

# import models
from apps.statistics.models import UnitRank, FinancialYear, FinancialQuarter

class DashboardView(UnicornView):
    court_rank = None
    financial_year = None
    quarter = None
    unit_ranks = None
    financial_years = None
    financial_quarters = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit_ranks =  UnitRank.objects.all()
        

    def changeCourtRank(self):
        if self.court_rank:
            self.financial_years = FinancialYear.objects.all()
            self.financial_year = None
            self.quarter = None
            self.financial_quarters = None
   

    def changeFinancialYear(self):
        if self.financial_year:
            self.financial_quarters = FinancialQuarter.objects.filter(financial_year=self.financial_year)
            self.quarter = None

    def changeQuarter(self):
        print(self.quarter)
        if self.quarter:
            return redirect('statistics:rank_units', self.court_rank, self.financial_year, self.quarter)