import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_dcrt_filepath(unit_rank, fy, month, unit, base_dir=None, extension=".xlsx"):
    """
    Constructs the structured filepath for a DCRT Excel file.
    Pattern: DCRT/TEMPLATE {rank_id}/{unit name}/{year}/{month}/{unique_code}.xlsx
    Example: DCRT/TEMPLATE 4/Kisumu ELRC/2024/01/KSMERC.xlsx
    """
    try:
        import glob

        if base_dir is None:
            base_dir = os.path.join(settings.BASE_DIR, 'DCRT')

        # Map month names to their numbers in file system
        month_numbers = {
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12',
            'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06'
        }
        month_str = month_numbers[month.name]
        
        # For Q1 months (July-September), use the first year of financial year
        # For other months, use second year
        if month.name in ['July', 'August', 'September']:
            year = fy.name.split('/')[0]  # Use first year (e.g., "2024" from "2024/2025")
        else:
            year = fy.name.split('/')[1]  # Use second year (e.g., "2025" from "2024/2025")
            
        logger.info(f"Processing month: {month.name} ({month_str}), year: {year}")
        
        # First look for files in this unit's directory
        unit_pattern = os.path.join(
            base_dir,
            f"TEMPLATE {unit_rank.id}",
            f"*{unit.name}*",  # Allow partial matches of unit name
            year,
            month_str,
            "*.xlsx"
        )
        logger.info(f"Checking unit pattern: {unit_pattern}")
        
        # Look for existing files in unit's directory
        unit_files = glob.glob(unit_pattern)
        if unit_files:
            logger.info(f"Found file in unit directory: {unit_files[0]}")
            return unit_files[0]
        
        # Look for template files in other court directories
        template_pattern = os.path.join(
            base_dir,
            f"TEMPLATE {unit_rank.id}",
            "*",  # Any court directory
            year,
            month_str,
            "*.xlsx"
        )
        logger.info(f"Checking template pattern: {template_pattern}")
        
        # Look for template files
        template_files = glob.glob(template_pattern)
        if template_files:
            logger.info("Available template files:")
            for template in template_files:
                court_dir = os.path.basename(os.path.dirname(os.path.dirname(template)))
                logger.info(f"- {court_dir}: {os.path.basename(template)}")
            selected_template = template_files[0]
            logger.info(f"Using template file: {selected_template}")
            return selected_template
        
        # If no existing files found, construct expected path for new file
        expected_path = os.path.join(
            base_dir,
            f"TEMPLATE {unit_rank.id}",
            unit.name,
            year,
            month_str,
            f"{unit.unique_code}{extension}"
        )
        logger.info(f"No existing files found. Using new path: {expected_path}")
        return expected_path

    except AttributeError as e:
        logger.error(f"Invalid attribute access while constructing path: {e}")
        return None
    except Exception as e:
        logger.error(f"Error generating DCRT filepath: {e}")
        return None