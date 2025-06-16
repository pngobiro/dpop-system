import os
import glob
import logging
from typing import Optional, Tuple, List
from django.conf import settings

# Fixed: Added __name__ instead of undefined 'name'
logger = logging.getLogger(__name__)

class DCRTFileChecker:
    """Utility class to check for DCRT Excel files in the filesystem"""
    
    def __init__(self):  # Fixed: Proper __init__ method
        """Initialize DCRT file checker with possible base paths"""
        self.possible_bases = [
            '/code/DCRT',  # Container path
            os.path.join(settings.BASE_DIR, 'DCRT'),  # Local path
            './DCRT'  # Relative path
        ]
        self.base_dir = self._find_dcrt_base()
    
    def _find_dcrt_base(self) -> str:  # Fixed: Proper method name with underscore
        """Find the valid DCRT base directory"""
        for base in self.possible_bases:
            logger.info(f"Checking DCRT base path: {base}")
            if os.path.exists(base):
                logger.info(f"Found valid DCRT base: {base}")
                return base
        logger.error("Could not find valid DCRT base directory")
        return self.possible_bases[0]  # Default to container path
    
    def get_template_folder(self, unit_rank_id: int) -> int:
        """Get template folder number based on unit rank"""
        return 4 if unit_rank_id in [4, 5] else unit_rank_id
    
    def get_year_for_quarter(self, financial_year: str, quarter_number: int) -> str:
        """Get the appropriate year based on financial year and quarter"""
        year_parts = financial_year.split('/')
        # Q3 (Jan-Mar) uses second year of financial year
        # Add your logic here for determining the year based on quarter
        if quarter_number == 3:
            return year_parts[1] if len(year_parts) > 1 else year_parts[0]
        else:
            return year_parts[0]  # Default to first year for other quarters