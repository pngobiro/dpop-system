import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from apps.statistics.models import (
    UnitRank, FinancialYear, FinancialQuarter,
    Unit, Division, Months
)
from apps.statistics.utils.dcrt_file_checker import DCRTFileChecker

logger = logging.getLogger(__name__)

def rank_unit_division_months(request, id, financial_year_id, financial_quarter_id, unit_id, division_id):
    """View for displaying months and verifying DCRT files for a specific unit and division."""
    try:
        # Get objects using get_object_or_404 for better error handling
        unit_rank = get_object_or_404(UnitRank, id=id)
        fy = get_object_or_404(FinancialYear, id=financial_year_id)
        fq = get_object_or_404(FinancialQuarter, id=financial_quarter_id)
        unit = get_object_or_404(Unit, id=unit_id)
        division = get_object_or_404(Division, id=division_id)
        
        # Log unit and division details
        logger.info(f"Unit details:")
        logger.info(f"- Name: {unit.name}")
        logger.info(f"- ID: {unit.id}")
        logger.info(f"- DCRT ID: {unit.dcrt_unique_id}")
        logger.info(f"- Unit Rank: {unit.unit_rank.name} (ID: {unit.unit_rank.id})")
        
        logger.info(f"Division details:")
        logger.info(f"- Name: {division.name}")
        logger.info(f"- ID: {division.id}")
        logger.info(f"- Code: {division.code}")
        
        # Initialize DCRT file checker
        dcrt_checker = DCRTFileChecker()
        
        # Get months for the quarter with error handling
        months_in_quarter = Months.objects.filter(financial_quarter=fq.quarter_number).order_by('month_number')
        if not months_in_quarter.exists():
            messages.warning(request, f"No months found for quarter {fq.quarter_number}")
            
        template_folder = dcrt_checker.get_template_folder(unit_rank.id)
        months_data = []
        
        dcrt_unique_id = getattr(unit, 'dcrt_unique_id', None)
        if not dcrt_unique_id:
            messages.warning(request, f"No DCRT ID found for unit {unit.name}")
            
        # Get appropriate year based on quarter
        year = dcrt_checker.get_year_for_quarter(fy.name, fq.quarter_number)
        logger.info(f"Using year {year} for Q{fq.quarter_number}")
        
        for month in months_in_quarter:
            logger.info(f"Checking month {month.name} ({month.month_number:02d}) in year {year}")
            
            file_exists = False
            found_file_path = None
            
            if dcrt_unique_id:
                # Check for DCRT file
                file_exists, found_file_path = dcrt_checker.check_dcrt_file(
                    unit_name=unit.name,
                    template_folder=template_folder,
                    year=year,
                    month=str(month.month_number),
                    dcrt_id=dcrt_unique_id
                )
                
                # Log directory structure for debugging
                dcrt_checker.log_directory_structure(
                    template_folder=template_folder,
                    unit_name=unit.name,
                    year=year,
                    month=str(month.month_number)
                )
                
                if file_exists:
                    logger.info(f"Found file for {month.name}: {found_file_path}")
            
            month_info = {
                'month': month,
                'month_number': month_str,
                'month_id': month.id,
                'file_exists': file_exists,
                'file_path': found_file_path
            }
            months_data.append(month_info)
        
        # Verify all required context variables are present
        if not all([unit_rank, fy, fq, unit, division]):
            error_msg = "Missing required context variables"
            logger.error(error_msg)
            messages.error(request, error_msg)
            raise ValueError(error_msg)

        # Update context with all necessary data, including IDs for URL reversing
        context = {
            'segment': 'statistics',
            'months_data': months_data,
            'unit_rank': unit_rank,
            'unit_rank_id': unit_rank.id,  # Add explicit ID
            'financial_year': fy,
            'financial_year_id': fy.id,  # Add explicit ID
            'financial_quarter': fq,
            'financial_quarter_id': fq.id,  # Add explicit ID
            'unit': unit,
            'unit_id': unit.id,  # Add explicit ID
            'division': division,
            'division_id': division.id,  # Add explicit ID
            'last_checked': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        logger.info("Context IDs for URL reversing:")
        logger.info(f"unit_rank_id: {unit_rank.id}")
        logger.info(f"financial_year_id: {fy.id}")
        logger.info(f"financial_quarter_id: {fq.id}")
        
        return render(request, 'statistics/rank_unit_months.html', context)
        
    except Exception as e:
        logger.error(f"Error in rank_unit_division_months: {str(e)}")
        messages.error(request, f"An error occurred while processing the request: {str(e)}")
        return render(request, 'statistics/rank_unit_months.html', {
            'segment': 'statistics',
            'error_message': str(e)
        })