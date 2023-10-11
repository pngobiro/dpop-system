import os
import openpyxl
from django.conf import settings
from openpyxl.utils import get_column_letter
from .models import DcrtData

def handle_uploaded_file(excel_file, id, financial_year_id, financial_quarter_id, unit_id, division_id, month_id):
    # Define the destination directory within MEDIA_ROOT where the file will be saved
    destination = os.path.join(settings.MEDIA_ROOT, 'uploads', excel_file.name)

    # Open and save the file to the destination
    with open(destination, 'wb+') as destination_file:
        for chunk in excel_file.chunks():
            destination_file.write(chunk)

    # Load the uploaded Excel file
    workbook = openpyxl.load_workbook(destination)
    worksheet = workbook.active

    # Start reading data from row 6, column B
    for row in worksheet.iter_rows(min_row=6, min_col=2, values_only=True):

        # if all values in the row are None, stop reading
        if all([cell is None for cell in row]):
            break
        else:
        # Create a DcrtData object and populate its fields
            dcrt_data = DcrtData(
                unit_id=unit_id,
                financial_year_id=financial_year_id,
                financial_quarter_id=financial_quarter_id,
                month_id=month_id,
                division_id=25,
                today_date_day=row[0],
                today_date_month=row[1],
                today_date_year=row[2],
                case_number_code = row[3],
                case_number_number = row[4],
                case_number_day = row[5],
                case_number_month = row[6],
                case_number_year = row[7],
                appeal_number_court_name = row[8],
                appeal_number_code = row[9],
                appeal_number_number = row[10] if row[10] else None,
                appeal_number_year = row[11] if row[11] else None,
                specific_case_type = row[12],
                judicial_officer_1 = row[13],
                judicial_officer_2 = row[14],
                judicial_officer_3 = row[15],
                judicial_officer_4 = row[16],
                judicial_officer_5 = row[17],
                judicial_officer_6 = row[18],
                judicial_officer_7 = row[19],
                judicial_officer_8 = row[20],
                case_coming_for = row[21],
                case_outcome = row[22],
                adjournment_reason = row[23],
                date_of_next_activity_day = row[24] if row[24] else None,
                date_of_next_activity_month = row[25] if row[25] else None,
                date_of_next_activity_year = row[26] if row[26] else None,
                no_of_plaintiffs_or_appellants_male = row[27] if row[27] else None,
                no_of_plaintiffs_or_appellants_female = row[28] if row[28] else None,
                no_of_plaintiffs_or_appellants_organization = row[29] if row[29] else None,
                no_of_defendants_accused_male = row[30] if row[30] else None,
                no_of_defendants_accused_female = row[31] if row[31] else None,
                no_of_defendants_accused_organization = row[32] if row[32] else None,
                parties_have_legal_representation = row[33] if row[33] else None,
                no_of_witnesses_in_court_d = row[34] if row[34] else None,
                no_of_witnesses_in_court_w = row[35] if row[35] else None,
                no_of_accused_remanded = row[36] if row[36] else None,
                last_date_of_submission_of_case_file_day = row[37] if row[37] else None,
                last_date_of_submission_of_case_file_month = row[38] if row[38] else None,
                last_date_of_submission_of_case_file_year = row[39] if row[39] else None,
                remarks = row[40],
            )
            dcrt_data.save()

    # Return the path where the file was saved
    return destination
