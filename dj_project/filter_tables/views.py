import os
import pdfplumber
import requests
import time

from django.conf import settings
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import render_to_string

from dotenv import load_dotenv

from pathlib import Path
from pypdf import PdfReader

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tqdm import tqdm

from filter_tables.models import TableName

from robot_sharepoint.modules.robot_for_login_and_download_from_sharepoint import robot_for_sharepoint
from robot_sharepoint.modules.recursive_robot import recursive_robot

# from management_before_django.robot_sharepoint.robot_for_outlook_exchangelib import func_for_search

# # While there's no model:
# model_dir = './models.py'
# count = 1
# do_we_have_tablename = False

# while not do_we_have_tablename:
#     try:
#         from .models import TableName
#         do_we_have_tablename = True
#     except ImportError:
#         print(count)
#         time.sleep(count)
#         count += 1
#     # module = __import__('models', fromlist=[''])
#     # do_we_have_tablename = hasattr(module, 'TableName')
    
# from .serializers import EmailSerializer

import ipdb

load_dotenv()

# ENVS:
# Keys for login:
username = os.getenv("USERN")
password = os.getenv("PASSWORD")

# Input ids:
hover_selector = os.getenv("HOVER_SELECTOR")
download_selector = os.getenv("DOWNLOAD_SELECTOR")

# Sharepoint URL:
sharepoint_url = os.getenv("SHAREPOINT_URL")

# Download directory:
download_directory = os.getenv("DOWNLOAD_DIRECTORY")

host_email = os.getenv("EMAIL_HOST_USER")

# Table to work with:
table_data = TableName.objects.all()

# ipdb.set_trace()
print("Views:", __name__)


class EmailAttachByTable(APIView):
    def post(self):
        try:
            counter = 0
            for row in tqdm(table_data, "Each line, each search and email"):
                # print(row)
                if counter == 0:
                    counter += 1
                    continue
                else:
                    cnpj = row.cnpj
                    nfe = row.numero
                    razao_social = row.nome_do_cliente
                    valor_liquido = row.valor_liquido
                    vencimento = row.dt_vencto

                    row_data = {
                        "cnpj": cnpj, 
                        "nfe": nfe, 
                        "razao_social": razao_social, 
                        "valor_liquido": valor_liquido, 
                        "vencimento": vencimento, 
                        "contact": "andrekuratomi@gmail.com"
                    }

                    # # TAKING INPUT IDS WITH SELENIUM ROBOT:
                    # input_ids = recursive_robot(username, sharepoint_url)
                    # print(input_ids)
                    
                    # # PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
                    # robot_for_sharepoint(
                    #     username,
                    #     password,
                    #     input_ids["user_input_id"],
                    #     input_ids["password_input_id"],
                    #     sharepoint_url,
                    #     download_directory,
                    #     # cnpj,
                    #     # nfe,
                    #     "02390435000115",
                    #     "17779"
                    # )
                    
                    # Extract info from attachments:
                    path = Path("./robot_sharepoint/attachments/")
                    # print(path)
                    tables_path_content = list(path.iterdir())

                    competencia_por_ano = ""
                    nome_do_cliente = ""
                    tipo_de_servico = ""
                    table_template = "table_template_deposito.html"

                    for file in tables_path_content:
                        # print(file)
                        string_file = str(file)
                        string_file_filtered = string_file[29:]
                        # print(string_file)
                        if string_file_filtered.startswith("NFE"):
                            specific_char_1 = "-"
                            specific_char_2 = "."
                            index_hifen = string_file_filtered.rfind(specific_char_1)
                            index_dot = string_file_filtered.rfind(specific_char_2)

                            nome_do_cliente = string_file_filtered[index_hifen+2:index_dot]
                            tipo_de_servico = string_file_filtered[10:index_hifen-1]
                            
                            # def convert_to_pure_pdf(input_path, output_path):
                            #     with pdfplumber.open(input_path) as pdf:
                            #         pages = pdf.pages
                            #         # Create a new PDFPlumber object for writing
                            #         writer = pdfplumber.PDFWriter(output_path)

                            #         for page in pages:
                            #             # Add each page to the writer object
                            #             writer.add_page(page)
                                    
                            #         # Save the output PDF file
                            #         writer.write()
                            # convert_to_pure_pdf(file, file)
                            
                            # Extract info from PDF:
                            pdf_content = PdfReader(file)
                            page = pdf_content.pages[0]
                            text = page.extract_text()
                            ipdb.set_trace()
                            # .pages[0]
                            print(text)

                        elif string_file.startswith("BOLETO"):
                            table_template = "table_template_boleto.html"

                    print("tipo_de_servico:", tipo_de_servico)
                    print("nome_do_cliente:", nome_do_cliente)

                    
                    # código para extrair a competência por ano do pdf

                    print("table_template:", table_template)

                    # Insert table to mail body:
                    mail_content = render_to_string(
                        table_template, {
                            'competencia_por_ano': competencia_por_ano, 
                            'nfe': row_data['nfe'], 
                            'nome_do_cliente': nome_do_cliente, 
                            'contact': row_data['contact'], 
                            'tipo_de_servico': tipo_de_servico
                        }
                        #  , using='ISO-8859-1'
                    )
                    # print(mail_content)
                    time.sleep(2)  # wait for file to be created

                    # ipdb.set_trace()
                    email = EmailMessage(
                        "Nota Fiscal Eletrônica - J&C Faturamento - {a1}  {a2}  ( {a3} )  NF -  -  - {a4}"
                        .format(
                            a1=row_data['tipo_de_servico'], 
                            a2=row_data['competencia_por_ano'], 
                            a3=row_data['nome_do_cliente'], 
                            a4=row_data['nfe']
                        ),
                        # "Envio tabela  {a1} - Novelis".format(a1=row_data['receiver_name']),
                        "",
                        "{}".format(host_email), 
                        [row_data['contact']], 
                        fail_silently=False,
                        html_message=mail_content
                    )

                    # Attach files to email:
                    for file in tables_path_content:
                        print(file)
                        str(file)
                        email.attach_file(file)

                    email.send()
                    print("Email successfully sent! Check inbox.")

                    # return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"error:Something went wrong! {e} Contact the dev!")
            # return Exception({"error": "Something went wrong! Contact the dev!"})


# class SendEmailView(APIView):
#     def post(self, row_data):
#         print("I")
#         ipdb.set_trace()
#         print("AM")
        
