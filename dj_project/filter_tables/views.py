import os
import fitz
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
    def post(self, root_dir: str):
        print(f"root_dir: {root_dir}")
        try:
            counter = 0
            
            final_not_found_list = "not_found_list.txt"
            not_found_list = "Not found elements: \n"

            with open(final_not_found_list, "w") as file:
                file.write(not_found_list)

            for row in tqdm(table_data, "Each line, each search and email"):
                # print(row)
                if counter == 0:
                    counter += 1
                    continue
                else:
                    cnpj = row.cnpj
                    nfe = row.numero
                    nome_do_cliente = row.nome_do_cliente
                    valor_liquido = row.valor_liquido
                    vencimento = row.dt_vencto

                    row_data = {
                        "cnpj": cnpj, 
                        "nfe": nfe, 
                        "nome_do_cliente": nome_do_cliente, 
                        "valor_liquido": valor_liquido, 
                        "vencimento": vencimento, 
                        # "contact": contato,
                        # "competencia_por_ano": "competencia_por_ano",
                        "contact": "andrekuratomi@gmail.com"
                    }
                    # print(row_data["contact"])

                    # TAKING INPUT IDS WITH SELENIUM ROBOT:
                    input_ids = recursive_robot(username, sharepoint_url)
                    print(input_ids)
                    
                    # PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
                    robot_for_sharepoint(
                        username,
                        password,
                        input_ids["user_input_id"],
                        input_ids["password_input_id"],
                        sharepoint_url,
                        download_directory,
                        cnpj,
                        nfe,
                        # "11068167000453", # boleto
                        # "17774" # boleto
                        # "02390435000115",
                        # "17779"
                        # "61102778000872", # not_found
                        # "17757" # not_found
                    )
                    # print(f"File: {__file__}")
                    attachments_path = "/robot_sharepoint/attachments/"
                    full_attachments_path = root_dir + attachments_path

                    # Extract info from attachments:
                    path = Path(full_attachments_path)
                    tables_path_content = list(path.iterdir())

                    competencia_por_ano = "02/01/2024"
                    # competencia_por_ano = ""
                    tipo_de_servico = ""
                    table_template = "table_template_deposito.html"

                    # bolar lista de cnpjs e/ou nfes não encontradas. criar string da lista vazia 
                    # para cada cnpj e/ou nfe elaborar uma string e acrescentar a essa lista
                    # no final da listagem. transformar a string da lista em um arquivo txt pelo comando 'string_lista >> algo.txt'
                    
                    # NOT FOUND CNPJ AND/OR NFE:
                    if len(tables_path_content) == 0:
                        not_found_elem = f"CNPJ: {cnpj} and/or NFE {nfe}. \n"
                        # table_template = "table_template_nao_encontrado.html"
                        
                        # not_found_list += not_found_elem
                        # print(not_found_list)
                        
                        with open(final_not_found_list, "a") as file:
                            file.write(not_found_elem)

                    else:
                        # ipdb.set_trace()
                        for file in tables_path_content:
                            print(file)
                            if file.is_file():
                                string_file = str(file)
                                # string_file_filtered = string_file[29:]
                                prefix = full_attachments_path
                                filtered = string_file[len(prefix):]
                                print("filtered:", filtered)
                                # print(string_file)
                                if filtered.startswith("NFE"):

                                    specific_char_1 = "-"
                                    specific_char_2 = "."
                                    specific_char_3 = " "
                                    # index_hifen = filtered.rfind(specific_char_1)
                                    # index_dot = filtered.rfind(specific_char_2)
                                    # nome_do_cliente = filtered[index_hifen+2:index_dot]

                                    tipo_de_servico = ""
                                    for charac in filtered[10:]:
                                        if charac == specific_char_2 or charac == specific_char_3:
                                            break
                                        else:
                                            tipo_de_servico += charac
                                    # tipo_de_servico = filtered[10:index_hifen-1]
                                    # ipdb.set_trace()

                                elif filtered.startswith("BOLETO"):
                                    table_template = "table_template_boleto.html"
                            
                            else:
                                print("Error! Verify the file.")

                        print("competencia_por_ano:", competencia_por_ano)
                        # ipdb.set_trace()
                        print("nome_do_cliente_data:", row_data['nome_do_cliente'])
                        print("table_template:", table_template)
                        print("tipo_de_servico:", tipo_de_servico)
                        # Insert table to mail body:
                        mail_content = render_to_string(
                            table_template, {
                                'competencia_por_ano': competencia_por_ano, 
                                'contact': row_data['contact'], 
                                'nfe': row_data['nfe'], 
                                # 'nfe': '17774', 
                                'nome_do_cliente':  row_data['nome_do_cliente'],
                                'tipo_de_servico': tipo_de_servico,
                                'valor_liquido': row_data['valor_liquido'],
                                'vencimento': row_data['vencimento']
                            }
                            #  , using='ISO-8859-1'
                        )
                        # print(mail_content)
                        time.sleep(2)  # wait for file to be created

                        # ipdb.set_trace()
                        email = EmailMessage(
                            "Nota Fiscal Eletrônica - J&C Faturamento - {a1}  {a2}  ( {a3} )  NF -  -  - {a4}"
                            .format(
                                a1=tipo_de_servico, 
                                a2=competencia_por_ano,
                                a3=row_data['nome_do_cliente'], 
                                # a4='17774'
                                a4=row_data['nfe']
                            ),
                            # "Envio tabela  {a1} - Novelis".format(a1=row_data['receiver_name']),
                            mail_content,
                            # "",
                            "{}".format(host_email), 
                            [row_data['contact']],
                            # attachments=tables_path_content
                            # [row_data['contact']], 
                            # fail_silently=False,
                        )
                        
                        # Reading HTML tags:
                        email.content_subtype = 'html'

                        # Attach files to email:
                        for file in tables_path_content:
                            print(file)
                            str(file)
                            email.attach_file(file)

                        email.send()
                        print("Email successfully sent! Check inbox.")

        except Exception as e:
            print(f"error:Something went wrong: {e} ! Contact the dev!")
            # return Exception({"error": "Something went wrong! Contact the dev!"})
