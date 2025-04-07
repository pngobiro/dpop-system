from django_unicorn.components import UnicornView
from django.shortcuts import redirect
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
        # Initialize dropdown options
        self.unit_ranks = UnitRank.objects.all()
        self.financial_years = FinancialYear.objects.all()
        # Quarters are loaded dynamically based on year selection

    def changeCourtRank(self):
        # When rank changes, reset year and quarter, reload years (though they don't change here)
        if self.court_rank:
            self.financial_years = FinancialYear.objects.all() # Or filter if needed
        self.financial_year = None
        self.quarter = None
        self.financial_quarters = None # Clear quarters

    def changeFinancialYear(self):
        # When year changes, reset quarter and load relevant quarters
        if self.financial_year:
            self.financial_quarters = FinancialQuarter.objects.filter(
                financial_year=self.financial_year
            ).order_by('quarter_number')
        else:
            self.financial_quarters = None
        self.quarter = None # Reset quarter selection

    def changeQuarter(self):
        if self.court_rank and self.financial_year and self.quarter:
            try:
                # Fetch the actual objects using the stored IDs
                rank_obj = UnitRank.objects.get(id=self.court_rank)
                fy_obj = FinancialYear.objects.get(id=self.financial_year)
                fq_obj = FinancialQuarter.objects.get(id=self.quarter)

                # Redirect to the rank view with selected parameters
                return redirect('statistics:rank_units',
                                id=rank_obj.id,
                                financial_year_id=fy_obj.id,
                                financial_quarter_id=fq_obj.id)
            except (UnitRank.DoesNotExist, FinancialYear.DoesNotExist, FinancialQuarter.DoesNotExist):
                # Handle cases where the selected ID might be invalid (optional, but good practice)
                # You might want to add a message to the user or log this error
                pass # Or handle appropriately