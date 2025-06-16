import os
import logging
from django.conf import settings
from .dcrt_file_checker import DCRTFileChecker
from apps.organization.models import Unit  # Import Unit model

logger = logging.getLogger(__name__)

def handle_uploaded_file(file, year, month, unit_id):
    """
    Handle the uploaded DCRT Excel file.
    
    Args:
        file: The uploaded file object
        year: The year for the DCRT data
        month: The month for the DCRT data
        unit_id: The ID of the unit submitting the data
        
    Returns:
        tuple: (bool, str) indicating success/failure and a message
    """
    try:
        # Get the unit object from database
        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            return False, f"Unit with ID {unit_id} not found"
            
        # Create the directory path based on the template format and unit rank
        dir_path = os.path.join(settings.DCRT_ROOT, f'TEMPLATE {unit.rank.id}')
        
        # Use the unit name for the folder
        unit_folder = unit.name
        
        # Create the full path including year and month
        full_path = os.path.join(dir_path, unit_folder, str(year), f"{month:02d}")
        
        # Create directories if they don't exist
        os.makedirs(full_path, exist_ok=True)
        
        # Generate filename using unit's unique code
        filename = f"{unit.unique_code}.xlsx"
        file_path = os.path.join(full_path, filename)
        
        # Save the file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Validate the uploaded file
        checker = DCRTFileChecker(file_path)
        validation_result = checker.validate()
        
        if validation_result['is_valid']:
            return True, "File uploaded and validated successfully"
        else:
            # If validation fails, remove the file
            os.remove(file_path)
            return False, f"Validation failed: {validation_result['errors']}"
            
    except Exception as e:
        logger.error(f"Error handling uploaded file: {str(e)}")
        return False, f"Error processing file: {str(e)}"