import os
import time

from django.core.mail import EmailMessage, mail_admins
from django.template.loader import render_to_string

from openpyxl import load_workbook
from pathlib import Path
from rest_framework.views import APIView
from tqdm import tqdm

from management_before_django.table_managements.modules.openpyxl_module import colect_data_and_reset_due_date, status_update
from management_before_django.table_managements.modules.paths_module import paths_with_file_name, paths_with_many_file_names

not_found = True
count = 0
while not_found:
    print(count)
    try:
        print("oi")
        from model_to_email.models import TableName
        not_found = False
    except ImportError:
        count += 1
        time.sleep(1)
        continue
print("TableName:", TableName)

from robot_sharepoint.modules.robots.robot_to_download_attachments import download_attachments_from_sharepoint
from robot_sharepoint.modules.robot_utils.join_reports import join_reports

from utils.functions.deleting_elements import do_we_have_things_to_delete
from utils.variables.envs import user_email, password, invoice_email, sheet, sharepoint_measurements_url, download_directory, host_email
from utils.variables.paths import edited_tables_path, models_file_path, raw_tables_path, reports_path
from utils.variables.report_files import not_found_list, sent_list, not_found_title, sent_title


import ipdb

# Table to work with:
table_data = TableName.objects.all()
print("table_data:", table_data)

print("Views:", __name__)


class EmailAttachByTable(APIView):
    def post(self, root_dir: str):
        """
            Extracts data from model, from each row of this data triggers selenium 'robot' for looking for attachments.
            If succesful, elaborates the email with the templates according to their content, attaches the files downloaded and send the email while register the successful case in the sent report.
            If not, the unsuccessful case is registered in the not sent report.
            At the end of the process a final report is made and sent triggering selenium 'robot' for uploading it.
        """

        try:
            # Not found list report creation:
            with reports_path.joinpath(not_found_list).open("w") as file:
                file.write(not_found_title)

            for row in tqdm(table_data, "Each line, each search and email"):
                client_id = row.client_id
                contact = row.contacts
                invoice = row.number
                clients_name = row.clients_name
                references = row.references
                status = row.status
                net_value = row.net_value
                due_date = row.due_date

                # logic for bug due_date = 31-12-1969:

                if due_date[6:8] != "20":
                    coluna_dt_due_date: int = 11
                                        
                    (contacts, complete_file_path_to_raw, file_path_to_raw) = paths_with_many_file_names(raw_tables_path)
                    # Workbooks:
                    workbook_all_raw_data = load_workbook(data_only=True, filename=file_path_to_raw)
                    all_raw_data = workbook_all_raw_data[sheet]

                    # EDITED TABLE:
                    # Paths:
                    (complete_file_path_to_edited, file_path_to_edited) = paths_with_file_name(edited_tables_path)
                    # Workbooks:
                    workbook_all_edited_data = load_workbook(data_only=True, filename=file_path_to_edited)
                    all_edited_data = workbook_all_edited_data[sheet]

                    colect_data_and_reset_due_date(all_raw_data, all_edited_data, coluna_dt_due_date, complete_file_path_to_edited, workbook_all_edited_data)
                    # ipdb.set_trace()
                    
                    raise ValueError("ERROR!: Verify column 'Due_date'! Year altered for before 2000!")

                if status == "Not sent":

                    row_data = {
                        # "competency_by_year": "competency_by_year",
                        # "contact": contact,
                        "contact": "test_1@company.com",
                        "client_id": client_id, 
                        "invoice": invoice, 
                        "clients_name": clients_name,
                        "references": references,
                        "net_value": net_value, 
                        "due_date": due_date, 
                    }
                    
                    # Month and year extraction:
                    refs = str(row_data['references'])

                    # PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
                    download_attachments_from_sharepoint(
                        user_email,
                        password,
                        sharepoint_measurements_url,
                        download_directory,
                        client_id,
                        invoice,
                        refs
                    )

                    attachments_path = "/robot_sharepoint/attachments/"
                    full_attachments_path = root_dir + attachments_path

                    # Extract info from attachments:
                    path = Path(full_attachments_path)
                    tables_path_content = list(path.iterdir())

                    # competency_by_year = "02/01/2024"
                    service_type = ""
                    table_template = "table_template_deposit.html"

                    # NOT FOUND client_id AND/OR invoice:
                    if len(tables_path_content) <= 1:
                        
                        # Fill element not found list:
                        not_found_elem = f"client_id: {client_id} and/or invoice {invoice}. \n"
                        with reports_path.joinpath(not_found_list).open("a") as file:
                            file.write(not_found_elem)

                    else:

                        for file in tables_path_content:
                            if file.is_file():
                                string_file = str(file)

                                if string_file.endswith('.pdf') or string_file.endswith('.xlsx'):
                                    prefix = full_attachments_path
                                    filtered = string_file[len(prefix):]

                                    # invoice pdf title example: 'invoice 17757 FIX January24.pdf'

                                    if filtered.endswith('.pdf'):
                                        try:
                                            print("FILTERED:", filtered)

                                            if filtered.startswith("invoice"):

                                                # 'Service type' and 'competency by year' info extraction from invoice pdf title:
                                                service_type = ""
                                                for charac in filtered[10:]: # from 'invoice <invoice_number> ' on
                                                    if charac == ' ':
                                                        break
                                                    else:
                                                        service_type += charac

                                                competency_by_year = ""
                                                count = 0
                                                for charac in filtered:
                                                    if count == 3:
                                                        if charac == '.':
                                                            break
                                                        else:
                                                            competency_by_year += charac
                                                    if charac == ' ':
                                                        count += 1

                                            elif filtered.startswith("BILL"):
                                                table_template = "table_template_bill.html"

                                        except Exception as e:
                                            print(f"ERRO! The pdf file found '{filtered}' is neither an invoice nor a bill and cannot be processed.")

                            else:
                                print("Error! Verify the file.")

                        # Insert table to mail body:
                        mail_content = render_to_string(
                            table_template, {
                                'competency_by_year': competency_by_year, 
                                'contact': row_data['contact'], 
                                'invoice': row_data['invoice'], 
                                'clients_name':  row_data['clients_name'],
                                'service_type': service_type,
                                'net_value': row_data['net_value'],
                                'due_date': row_data['due_date']
                            }
                        )

                        time.sleep(2)  # wait for file to be created

                        email = EmailMessage(
                            "INVOICE - Company billings - {a1}  {a2}  ( {a3} )  NF -  -  - {a4}"
                            .format(
                                a1=service_type, 
                                a2=competency_by_year,
                                a3=row_data['clients_name'], 
                                a4=row_data['invoice']
                            ), # SUBJECT
                            mail_content, # BODY
                            "{}".format(host_email), # FROM
                            [row_data['contact']], # TO
                            [
                                invoice_email, 
                                "test_1@company.com"], # BCC
                        )
                        
                        # Reading HTML tags:
                        email.content_subtype = 'html'

                        # Attach files to email:
                        for file in tables_path_content:
                            print(file)
                            stringfy = str(file)
                            if stringfy.endswith('.pdf') or stringfy.endswith('.xlsx'):
                                email.attach_file(file)

                        email.send()
                        print("Email successfully sent! Check inbox.")

                        # Fill element sent list:
                        sent_elem = f"client_id: {client_id} and/or invoice {invoice}. \n"
                        with reports_path.joinpath(sent_list).open("a") as file:
                            file.write(sent_elem)

                        # STATUS UPDATE:
                        status_update(edited_tables_path, row_data)

                else:
                    continue

            # Delete raw_table content when the whole view process finishes:
            do_we_have_things_to_delete(raw_tables_path, '.xlsx')

            print("THE APPLICATION FINISHED THE EMAIL SENT PROCESS SUCCESSFULLY!")

        except Exception as e:
            print(f"error:Something went wrong: {e} ! Contact the dev!")
