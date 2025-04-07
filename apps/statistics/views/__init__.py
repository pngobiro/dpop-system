# Import the home view from dashboard module
from .dashboard import home

# Import views from modules
from .dashboard import (
    rank_units,
)

from .case_analysis import (
    case_summary,
    monthly_unit_registered_cases,
    monthly_unit_resolved_cases,
    rank_unit_division_month_cases_summary,
)

from .unit_views import (
    rank_unit_division_months,
    unit_division_quarters,
    unit_division_fy,
    monthly_unit_matters_handled,
    upload_unit_monthly_dcrt_excel,
)

from .data_quality import (
    monthly_unit_missing_data,
    monthly_unit_duplicate_data,
    monthly_unit_outliers,
    monthly_unit_incomplete_data,
)

# Export all views
__all__ = [
    # Main view
    'home',
    
    # Dashboard views
    'rank_units',
    
    # Case analysis views
    'case_summary',
    'monthly_unit_registered_cases',
    'monthly_unit_resolved_cases',
    'rank_unit_division_month_cases_summary',
    
    # Unit views
    'rank_unit_division_months',
    'unit_division_quarters',
    'unit_division_fy',
    'monthly_unit_matters_handled',
    'upload_unit_monthly_dcrt_excel',
    
    # Data quality views
    'monthly_unit_missing_data',
    'monthly_unit_duplicate_data',
    'monthly_unit_outliers',
    'monthly_unit_incomplete_data',
]