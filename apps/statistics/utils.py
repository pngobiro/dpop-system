import os
import openpyxl
from django.conf import settings
from openpyxl.utils import get_column_letter
from .models import DcrtData # Keep original model import
import logging

logger = logging.getLogger(__name__)

# Helper function to safely get value from row tuple
def get_value_from_row(row, index, expected_type=None, default=None):
    """Safely gets a value from a row tuple, attempts type conversion, and handles errors."""
    raw_value = None
    try:
        if index < len(row):
            raw_value = row[index]
            if raw_value is None:
                return default

            if expected_type == int:
                # Attempt to convert to int, handle potential errors
                try:
                    # Handle cases like '1.0' which are valid floats but should be int
                    if isinstance(raw_value, float) and raw_value.is_integer():
                         return int(raw_value)
                    return int(raw_value)
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert '{raw_value}' (type: {type(raw_value)}) to int for index {index}. Returning default.")
                    return default # Return default (None) if conversion fails
            elif expected_type == str:
                 return str(raw_value) # Ensure string type if needed
            # Add other type checks (float, date) if necessary
            else:
                return raw_value # Return raw value if no specific type needed
        else:
            # Index out of range
            return default
    except IndexError:
        # This case should be less likely with the len check, but keep for safety
        return default
    except Exception as e:
        logger.error(f"Unexpected error in get_value_from_row for index {index}, value '{raw_value}': {e}")
        return default
def handle_uploaded_file(uploaded_file, unit_rank, fy, fq, unit, division, month):
    """
    Handles uploaded Excel file, saves it to a structured path, and processes its data.
    Path: MEDIA_ROOT/TEMPLATE <rank_id>/<unit_name>/<year_name>/<month_number>/<unit_code>.xlsx
    """
def get_dcrt_filepath(unit_rank, fy, month, unit, base_dir=os.path.join(settings.BASE_DIR, 'DCRT'), extension=".xlsx"): # Changed base_dir default
    """Constructs the structured filepath for a DCRT Excel file."""
    try:
        # Sanitize names for directory creation
        unit_name_sanitized = "".join(c if c.isalnum() or c in (' ', '-') else '_' for c in unit.name)
        year_name_sanitized = fy.name.replace('/', '-') # Replace slashes in year name

        # Construct the relative path components
        relative_path = os.path.join(
            f"TEMPLATE {unit_rank.id}",
            unit_name_sanitized,
            year_name_sanitized,
            f"{month.month_number:02d}" # Use month number (padded) for folder
        )
        
        # Construct the filename using unit unique code
        filename = f"{unit.unique_code}{extension}"
        
        # Return the full path
        return os.path.join(base_dir, relative_path, filename)
        
    except Exception as e:
        logger.error(f"Error generating DCRT filepath for unit {unit.id}, month {month.id}: {e}")
        return None

def handle_uploaded_file(uploaded_file, unit_rank, fy, fq, unit, division, month):
    """
    Handles uploaded Excel file, saves it to a structured path, and processes its data.
    Path: MEDIA_ROOT/TEMPLATE <rank_id>/<unit_name>/<year_name>/<month_number>/<unit_code>.xlsx
    """
    try:
        # Use the helper function to get the destination path
        destination_path = get_dcrt_filepath(unit_rank, fy, month, unit, extension=os.path.splitext(uploaded_file.name)[1])
        
        if not destination_path:
            logger.error("Could not determine destination path for upload.")
            return None # Indicate save failure

        # Ensure the directory exists
        full_dir_path = os.path.dirname(destination_path)
        os.makedirs(full_dir_path, exist_ok=True)
        
        logger.info(f"Saving uploaded file to: {destination_path}")

        # Save the file
        with open(destination_path, 'wb+') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)
    except Exception as e:
        logger.error(f"Error saving uploaded file: {e}")
        # Decide how to handle save error (e.g., raise, return False)
        return None # Indicate save failure

    # --- Existing Excel processing logic ---
    try:
        # Load the saved Excel file
        workbook = openpyxl.load_workbook(destination_path)
        worksheet = workbook.active
        logger.info(f"Processing data from: {destination_path}")

        # Start reading data from row 6, column B
        row_count = 0
        for row_index, row in enumerate(worksheet.iter_rows(min_row=6, min_col=2, values_only=True), start=6):
            if all([cell is None for cell in row]):
                logger.info(f"Stopping processing at empty row {row_index}")
                break
            
            # Create a DcrtData object using the helper function for safety
            # Build data dictionary with type conversion attempts
            data_dict = {
                'today_date_day': get_value_from_row(row, 0, expected_type=int),
                'today_date_month': get_value_from_row(row, 1),
                'today_date_year': get_value_from_row(row, 2),
                'case_number_code': get_value_from_row(row, 3),
                'case_number_number': get_value_from_row(row, 4, expected_type=int),
                'case_number_day': get_value_from_row(row, 5, expected_type=int),
                'case_number_month': get_value_from_row(row, 6),
                'case_number_year': get_value_from_row(row, 7, expected_type=int),
                'appeal_number_court_name': get_value_from_row(row, 8),
                'appeal_number_code': get_value_from_row(row, 9),
                'appeal_number_number': get_value_from_row(row, 10, expected_type=int),
                'appeal_number_year': get_value_from_row(row, 11, expected_type=int),
                'specific_case_type': get_value_from_row(row, 12),
                'judicial_officer_1': get_value_from_row(row, 13),
                'judicial_officer_2': get_value_from_row(row, 14),
                'judicial_officer_3': get_value_from_row(row, 15),
                'judicial_officer_4': get_value_from_row(row, 16),
                'judicial_officer_5': get_value_from_row(row, 17),
                'judicial_officer_6': get_value_from_row(row, 18),
                'judicial_officer_7': get_value_from_row(row, 19),
                'judicial_officer_8': get_value_from_row(row, 20),
                'case_coming_for': get_value_from_row(row, 21),
                'case_outcome': get_value_from_row(row, 22),
                'adjournment_reason': get_value_from_row(row, 23),
                'date_of_next_activity_day': get_value_from_row(row, 24, expected_type=int),
                'date_of_next_activity_month': get_value_from_row(row, 25),
                'date_of_next_activity_year': get_value_from_row(row, 26, expected_type=int),
                'no_of_plaintiffs_or_appellants_male': get_value_from_row(row, 27, expected_type=int),
                'no_of_plaintiffs_or_appellants_female': get_value_from_row(row, 28, expected_type=int),
                'no_of_plaintiffs_or_appellants_organization': get_value_from_row(row, 29, expected_type=int),
                'no_of_defendants_accused_male': get_value_from_row(row, 30, expected_type=int),
                'no_of_defendants_accused_female': get_value_from_row(row, 31, expected_type=int),
                'no_of_defendants_accused_organization': get_value_from_row(row, 32, expected_type=int),
                'parties_have_legal_representation': get_value_from_row(row, 33),
                'no_of_witnesses_in_court_d': get_value_from_row(row, 34, expected_type=int),
                'no_of_witnesses_in_court_w': get_value_from_row(row, 35, expected_type=int),
                'no_of_accused_remanded': get_value_from_row(row, 36, expected_type=int),
                'last_date_of_submission_of_case_file_day': get_value_from_row(row, 37),
                'last_date_of_submission_of_case_file_month': get_value_from_row(row, 38),
                'last_date_of_submission_of_case_file_year': get_value_from_row(row, 39),
                'remarks': get_value_from_row(row, 40),
            }

            # Create and save DcrtData object
            try:
                DcrtData.objects.create(
                    unit=unit,
                    financial_year=fy,
                    financial_quarter=fq,
                    month=month,
                    division=division,
                    **data_dict # Unpack the cleaned dictionary
                )
                row_count += 1
            except Exception as e:
                # Log the specific data that caused the save error
                logger.error(f"Error saving row {row_index} data: {data_dict}. Error: {e}")
                # Decide whether to continue processing other rows or stop
                # continue # or break or raise e
        logger.info(f"Successfully processed {row_count} rows from Excel file.")
    except Exception as e:
        logger.error(f"Error processing Excel file {destination_path}: {e}")
        return None # Indicate processing failure

    # Removed duplicated code block that was causing NameError
