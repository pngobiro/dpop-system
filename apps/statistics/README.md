# Statistics App

This Django app handles data collection, analysis, and reporting for court case statistics and related metrics.

## Directory Structure

```
statistics/
│
├── utils/                     # Utility functions and helpers
│   ├── dcrt_file_checker.py  # DCRT Excel file validation
│   ├── dcrt_filepath.py      # DCRT file path management
│   ├── file_upload.py        # File upload handling
│   └── __init__.py          # Package exports
│
├── views/                     # View functions
│   ├── case_analysis.py      # Case analytics views
│   ├── dashboard.py          # Main dashboard views
│   ├── rank_unit_division_months.py # Unit ranking views
│   └── upload_unit_monthly_dcrt_excel.py # File upload views
│
└── templates/                 # HTML templates
    └── statistics/           # App-specific templates
```

## Core Features

1. DCRT File Management
   - File upload and validation
   - Structured file storage
   - Data extraction and processing

2. Data Analysis
   - Case summaries and statistics
   - Unit performance metrics
   - Monthly reports and comparisons

3. Visualization
   - Performance dashboards
   - Statistical charts and graphs
   - Ranking comparisons

## Key Components

### DCRT File Handling
- `DCRTFileChecker`: Validates uploaded Excel files
- `get_dcrt_filepath`: Manages standardized file paths
- `handle_uploaded_file`: Processes file uploads

### Data Analysis Views
- Case summary and analysis
- Monthly unit statistics
- Performance rankings
- Data quality checks

### File Path Convention
```
DCRT/
└── TEMPLATE <rank_id>/
    └── <unit_name>/
        └── <year>/
            └── <month>/
                └── <unit_code>.xlsx
```

Example: `DCRT/TEMPLATE 4/Kisumu ELRC/2024/01/KSMERC.xlsx`

## Usage

1. Uploading DCRT Files:
```python
from statistics.utils import handle_uploaded_file

result, message = handle_uploaded_file(
    file=uploaded_file,
    year=year,
    month=month,
    unit_id=unit_id
)
```

2. Accessing File Paths:
```python
from statistics.utils import get_dcrt_filepath

filepath = get_dcrt_filepath(
    unit_rank=rank,
    fy=financial_year,
    month=month,
    unit=unit
)
```

## Dependencies
- pandas: Data processing and analysis
- openpyxl: Excel file handling
- django-pandas: DataFrame integration with Django

## Import Guidelines
To avoid circular imports, follow these conventions:
1. Use absolute imports for models and views
   ```python
   from apps.statistics.models import Unit
   from apps.statistics.views.dashboard import home
   ```

2. Use relative imports within the utils package
   ```python
   from .dcrt_file_checker import DCRTFileChecker
   from .dcrt_filepath import get_dcrt_filepath
   ```

3. Import utility functions through the utils package
   ```python
   from apps.statistics.utils import get_dcrt_filepath, handle_uploaded_file
   ```

## Configuration
DCRT file storage location is configured in Django settings:
```python
DCRT_ROOT = os.path.join(BASE_DIR, 'DCRT')
```

## Version Control

### Repository Migration (Bitbucket to GitHub)
1. The new GitHub repository is ready at:
   ```
   https://github.com/pngobiro/dpop-system.git
   ```

2. Execute the migration script:
   ```bash
   # Make the script executable if needed
   chmod +x migration_steps.sh
   
   # Run the migration script
   ./migration_steps.sh
   ```

   The script will:
   - Add new statistics app files
   - Remove Excel files from git tracking
   - Update configuration files
   - Switch the remote to GitHub
   - Rename master branch to main
   - Push to the new repository

3. Manual verification after migration:
   ```bash
   # Verify the new remote
   git remote -v
   
   # Check repository status
   git status
   
   # Verify Excel files are not tracked
   git ls-files | grep xlsx
   ```

Note: The script:
1. Preserves all Excel files locally while removing them from git tracking
2. Creates a backup of sensitive files in `.sensitive_backup/` directory
3. Removes sensitive files from git tracking while keeping them locally
4. Updates `.gitignore` to prevent re-adding sensitive files

### Sensitive Files Handling
The following files are automatically protected:
- `client_secrets.json`
- Any files containing `credentials` in name
- Any files containing `secret` in name
- Environment files (`.env.*`)
- Key files (`*.key`)

After migration:
1. Verify sensitive files are in `.sensitive_backup/`
2. Check they are not tracked by git:
   ```bash
   git ls-files | grep -i "secret\|key\|password\|credential"
   ```
3. Update any file paths if needed

### Git Configuration
1. Excel files and data directories are ignored in `.gitignore`:
   ```gitignore
   # Excel and DCRT files
   *.xls
   *.xlsx
   *.xlsm
   *.xlsb
   DCRT/
   data/
   ```

2. To ensure Excel files are not tracked:
   ```bash
   # Remove Excel files from git tracking
   git rm --cached "*.xlsx"
   git rm --cached "*.xls"
   git rm -r --cached DCRT/
   
   # Commit the changes
   git commit -m "Remove Excel files from tracking"
   ```

3. For team members after migration:
   ```bash
   # Clone from new GitHub repository
   git clone https://github.com/username/repository.git
   
   # Update local repository if already cloned
   git remote set-url origin https://github.com/username/repository.git
   git fetch
   ```

## What's Next

### Immediate Tasks
1. Data Validation
   - [ ] Add comprehensive Excel file structure validation
   - [ ] Implement data type checks for all fields
   - [ ] Add validation for court-specific data formats

2. Performance Optimization
   - [ ] Add caching for frequently accessed reports
   - [ ] Optimize database queries in analysis views
   - [ ] Implement batch processing for large file uploads

3. Testing
   - [ ] Add unit tests for utility functions
   - [ ] Create integration tests for file upload process
   - [ ] Add test coverage for data analysis functions

### Future Enhancements
1. Data Processing
   - [ ] Add support for bulk file uploads
   - [ ] Implement automatic data correction suggestions
   - [ ] Add data versioning and change tracking

2. Reporting
   - [ ] Implement quarterly performance reports
      * Case resolution rates
      * Performance metrics by division
      * Quarter-over-quarter comparisons
   - [ ] Develop annual reports
      * Yearly performance summaries
      * Historical trend analysis
      * Year-over-year comparisons
   - [ ] Add ad-hoc report generation
      * Custom date range selection
      * Flexible metric combinations
      * Dynamic filtering options
   - [ ] Create individual unit reports
      * Unit-specific performance metrics
      * Comparative analysis with similar units
      * Custom export formats (PDF, Excel, Word)
   - [ ] Implement automated report scheduling
      * Scheduled quarterly reports
      * Annual report reminders
      * Report archiving system

3. User Experience
   - [ ] Add progress tracking for file uploads
   - [ ] Implement real-time validation feedback
   - [ ] Add interactive data visualization

### Maintenance
1. Code Quality
   - [ ] Regular dependency updates
   - [ ] Code style consistency checks
   - [ ] Documentation updates

2. Monitoring
   - [ ] Add error tracking and reporting
   - [ ] Implement performance monitoring
   - [ ] Add usage analytics

3. Security
   - [ ] Regular security audits
   - [ ] File upload vulnerability checks
   - [ ] Access control reviews