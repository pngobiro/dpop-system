      
# apps/pmmu/management/commands/seed_pmmu_from_ocr.py
from django.core.management.base import BaseCommand
from apps.pmmu.models import PerformanceIndicator, IndicatorNote, PMMU, IndicatorCategory, FinancialYearPerformance
from apps.statistics.models import FinancialYear
from apps.organization.models import Department
from django.contrib.auth import get_user_model
from apps.document_management.utils.document_manager import DocumentManager
from django.core.files.base import ContentFile
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds PMMU data with Indicators and IndicatorNotes from OCR text for multiple years'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding PMMU Indicator data with notes and document attachments from OCR text...')

        # --- Prerequisites ---
        financial_year_names = ["2020/2021", "2021/2022", "2022/2023", "2023/2024", "2024/2025"] # Define FYs to create

        directorate_dept = Department.objects.filter(name="Director's Office").first()
        if not directorate_dept:
            self.stdout.write(self.style.ERROR("Department 'Director's Office' not found. Run seed_organization first."))
            return

        uploaded_by_user = User.objects.filter(username='joseph.osewe').first() # Assuming a user exists to be creator of notes
        if not uploaded_by_user:
            self.stdout.write(self.style.ERROR("User 'joseph.osewe' not found. Create this user or adjust seeder."))
            return

        # --- Fetch or Create Indicator Categories ---
        indicator_categories_data = [
            {'name': 'core_mandate', 'display_name': 'A. CORE MANDATE'},
            {'name': 'financial_perspective', 'display_name': 'B. FINANCIAL PERSPECTIVE'},
            {'name': 'customer_perspective', 'display_name': 'C. CUSTOMER PERSPECTIVE'},
            {'name': 'innovation_learning', 'display_name': 'D. INNOVATION AND LEARNING'},
            {'name': 'internal_processes', 'display_name': 'E. INTERNAL PROCESSES'},
        ]
        indicator_categories = {}
        for cat_data in indicator_categories_data:
            category, created = IndicatorCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'display_name': cat_data['display_name']}
            )
            indicator_categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Indicator Category: {category.display_name}'))
            else:
                self.stdout.write(f'  Indicator Category already exists: {category.display_name}')


        for fy_name in financial_year_names: # Loop through financial years
            financial_year = FinancialYear.objects.filter(name=fy_name).first()
            if not financial_year:
                self.stdout.write(self.style.WARNING(f'Financial Year {fy_name} not found. Skipping.')) # Warning instead of Error, to continue seeding other years
                continue # Skip to the next FY if not found

            # --- Create PMMU Instance for each Financial Year ---
            pmmu_instance = PMMU.objects.create(
                name=f"Performance Management & Measurement Understanding {fy_name}", # Dynamic PMMU name
                financial_year=financial_year,
                description=f"This PMMU Understanding for FY {fy_name} outlines the agreement between The Chief Registrar of the Judiciary and The Director, Strategy Planning and Organizational Productivity.", # Dynamic description
            )
            self.stdout.write(self.style.SUCCESS(f'Created PMMU: {pmmu_instance.name}'))

            # --- Indicator Data (Extracted from OCR - Page 5 Schedule + Pages 6-8 Notes) ---
            indicators_data = [
                {'category': 'core_mandate', 'name': 'Institutionalize Performance Management', 'unit_of_measure': '%', 'weight': 10, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Review 2023-2024 performance management guidelines", "b. Coordinate PMMU evaluations and target setting to all courts and units within the first half of the financial year", "c. Coordinate PMMUs evaluation for all Implementing Units", "d. Evaluate compliance of Service Delivery Standards and prepare annual report", "e. Conduct annual Performance Management and Measurement sensitisation for Heads of Stations and Deputy Registrars", "f. Facilitate annual AJPMC engagement on status and feedback of PMMU implementation to improve the process.", "g. Undertake PMMU briefs for the following;", "a. Chief Justice", "b. Deputy Chief Justice", "c. Chief Registrar of the Judiciary", "d. Judiciary Management Team", "h. Identify and recommend new/reviewed performance measurement indicators and submit to AJPMC for adoption"]},
                {'category': 'core_mandate', 'name': 'Enhance Data Governance', 'unit_of_measure': '%', 'weight': 10, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Sensitize staff in at least 200 courts on data management.", "b. Facilitate case audits in 10 courts", "c. Improve caseload data accuracy across the Judiciary by 3 percent.", "d. Update the data dictionary in liaison with the registrars as need arises."]},
                {'category': 'core_mandate', 'name': 'Timely preparation and dissemination of caseload statistics', 'unit_of_measure': '%', 'weight': 10, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Annual Caseload Statistics Report for FY 2023/24 by 5th August 2024.", "b. 1st Quarter Caseload Report 2024/25 by 5th November 2024.", "c. 2nd Quarter Caseload Report 2024/25 by 5th February 2025.", "d. 3rd Quarter Caseload Report 2024/25 by 5th May 2025."]},
                {'category': 'core_mandate', 'name': 'Facilitate use of Statistics to inform policy', 'unit_of_measure': '%', 'weight': 5, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Prepare input on caseload statistics for the SOJAR Report 2023/24.", "b. Prepare and submit draft performance reports of individual Judges and Judicial officers for JSC within the timelines specified as per request."]},
                {'category': 'core_mandate', 'name': 'Institutionalize Quality Management Systems', 'unit_of_measure': '%', 'weight': 8, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Facilitate establishment of the Judiciary ISO-QMS Steering Committee", "b. Develop a Judiciary ISO-QMS Road Map", "c. Coordinate Development of ISO-QMS Procedures for NCAJ"]},
                {'category': 'core_mandate', 'name': 'Promote Service Delivery Innovations', 'unit_of_measure': '%', 'weight': 7, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Collate and review and publish Service Delivery Innovations", "b. Review and Disseminate Service Delivery Innovations for Replications", "c. Develop and Maintain a Service Delivery Innovations Online-Repository", "d. Undertake and disseminate 1 research on topical issue to inform policy"]},
                {'category': 'core_mandate', 'name': 'Enhance Reporting on Programs and Projects', 'unit_of_measure': '%', 'weight': 10, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Prepare and disseminate quarterly statistical reports within 30 days from the close of submission by courts", "b. Prepare and disseminate quarterly M&E reports within 5 days from receipt of statistical report", "c. Prepare ad-hoc reports within 7 days after receipt of the request", "d. Prepare 2023-2024 PMMUs evaluation report by 30th June 2025", "e. Evaluate the Judiciary Strategic Plan 2019-2023", "f. Track implementation of multi-door approach to justice programs such as AJS, CAM, and address emerging issues and report to management"]},
                {'category': 'core_mandate', 'name': 'Enhance Feedback Mechanism', 'unit_of_measure': '%', 'weight': 10, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Analyse Judiciary dialogue feedback and disseminate the findings", "b. Analyse field report from PMMU evaluation exercise and disseminate the findings to AJPMC and management"]},
                {'category': 'financial_perspective', 'name': 'Compliance with the budget', 'unit_of_measure': '%', 'weight': 3, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Ensure 100% absorption of the budget as per the approved work plan"]},
                {'category': 'financial_perspective', 'name': 'Greening Initiatives', 'unit_of_measure': '%', 'weight': 2, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["b. Implement energy saving initiatives"]}, # Note: 'b.' is used as it's continuation of 'Greening Initiatives' Section B.2
                {'category': 'customer_perspective', 'name': 'Compliance with Service Delivery Charter Standards', 'unit_of_measure': '%', 'weight': 5, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["The Directorate will track compliance of all the Service Delivery Charter standards"]},
                {'category': 'customer_perspective', 'name': 'Implement or follow-up on the implementation of the recommendations from the customer satisfaction survey', 'unit_of_measure': '%', 'weight': 5, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["The Directorate will conduct one survey that involves court users and disseminate the findings"]},
                {'category': 'innovation_learning', 'name': 'Service improvement Innovations', 'unit_of_measure': 'No.', 'weight': 4, 'target_2024_2025': '1', 'baseline_2023_2024': '1',
                 'notes': ["a. Replicate/adopt any relevant innovations OR", "b. May come up with one service delivery innovation"]},
                {'category': 'innovation_learning', 'name': 'Competency development', 'unit_of_measure': '%', 'weight': 6, 'target_2024_2025': 100, 'baseline_2023_2024': '3',
                 'notes': ["a. Identify training gaps and facilitate relevant training"]},
                {'category': 'internal_processes', 'name': 'Corruption Prevention & Eradication', 'unit_of_measure': '%', 'weight': 2, 'target_2024_2025': 100, 'baseline_2023_2024': '',
                 'notes': ["a. Continue sensitizing members of staff on dangers of corruption in staff meetings", "b. Document and maintain records of all reported corruption related issues from various sources including the following;", "Complaints/corruption feedback", "Oversight bodies", "C. Implement the recommendations of corruption prevalence surveys and system audits by DSPOP, EACC, and other public oversight bodies.", "d. Implement corruption prevention action plans by integrity officers and submit quarterly reports to OJO and OCRJ.", "e. Implement strategies to address reported and other corruption eradication activities."]},
                {'category': 'internal_processes', 'name': 'Improve Employee wellness', 'unit_of_measure': '%', 'weight': 1, 'target_2024_2025': 100, 'baseline_2023_2024': '',
             'notes': ["a. Implement staff welfare programme¹", "b. Organize one team building event for staff²"]}, # Note: Superscript numbers in OCR
                {'category': 'internal_processes', 'name': 'Enhance Employee Satisfaction and Work Environment', 'unit_of_measure': '%', 'weight': 2, 'target_2024_2025': 100, 'baseline_2023_2024': '',
             'notes': ["a. Hold quarterly staff meetings, emerging issues affecting staff welfare and report progress in the subsequent meetings.", "b. Conduct Employee Satisfaction and Work Environment Survey³ and disseminate the findings"]}, # Note: Superscript numbers in OCR
            ]


            # --- Create Indicator Items ---
            for indicator_data in indicators_data:
                category_name = indicator_data['category']
                indicator_category = indicator_categories.get(category_name) # Get IndicatorCategory object
                if not indicator_category:
                    self.stdout.warning(f"  Warning: Indicator Category '{category_name}' not found for indicator '{indicator_data['name']}'. Skipping indicator.")
                    continue # Skip to the next indicator if category is missing

                indicator = PerformanceIndicator.objects.create( # Updated model name to PerformanceIndicator
                    subcategory=indicator_category, # Assign IndicatorCategory
                    name=indicator_data['name'],
                    description=indicator_data.get('description', ''), # Description not in page 5, using empty string as default
                    unit_of_measure=indicator_data['unit_of_measure'],
                    weight=indicator_data['weight'],
                )
                self.stdout.write(self.style.SUCCESS(f'  Created PMMU Indicator: {indicator.name} (Category: {indicator_category.display_name})'))

                # --- Create FinancialYearPerformance for 2024-2025 (Last FY in list) ---
                if fy_name == financial_year_names[-1]: # Apply targets/baselines only to the last FY (2024-2025)
                    FinancialYearPerformance.objects.create(
                        financial_year=financial_year,
                        indicator=indicator,
                        target=indicator_data['target_2024_2025'],
                        baseline=indicator_data['baseline_2023_2024'] # Using baseline from indicators_data
                    )
                    self.stdout.write(self.style.SUCCESS(f'    Created FinancialYearPerformance for {fy_name}: {indicator.name}'))
                else: # For other FYs, create FinancialYearPerformance with default values
                    FinancialYearPerformance.objects.create(
                        financial_year=financial_year,
                        indicator=indicator,
                        target="N/A", # Or some default target value for other years
                        baseline="N/A" # Or default baseline
                    )
                    self.stdout.write(self.style.SUCCESS(f'    Created FinancialYearPerformance (default) for {fy_name}: {indicator.name}'))


                # --- Create Indicator Notes ---
                indicator_notes = indicator_data['notes'] # Now notes is a list
                for note_text in indicator_notes: # Iterate through the list of notes
                    indicator_note = IndicatorNote.objects.create(
                        indicator=indicator,
                        note_text=note_text.strip(), # Save each line as a separate note
                        created_by=uploaded_by_user # Assign creator for notes
                    )
                    self.stdout.write(self.style.SUCCESS(f'    Created Indicator Note: {note_text[:50]}...')) # Show truncated note text

                    # --- Attach Documents to Notes (Randomly) ---
                    if random.random() < 0.3:
                        doc_title = f"Document for Note: {indicator_note.note_text[:20]}..." # Title from note text
                        doc_content = fake.text(max_nb_chars=100)
                        doc_file = ContentFile(doc_content.encode('utf-8'), name=f"note_doc_{indicator.pk}_{indicator_note.pk}.txt") # Unique filename

                        DocumentManager.attach_document(
                            file=doc_file,
                            source_object=indicator_note,
                            uploaded_by=uploaded_by_user,
                            title=doc_title,
                            description=f"Dummy document attached to indicator note for {indicator.name}",
                            source_module='pmmu_app'
                        )
                        self.stdout.write(self.style.SUCCESS(f'      Attached document to Note: {doc_title}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded PMMU Indicator data from OCR text with PMMUs, Indicators, Notes, Categories and FY Performance Data'))