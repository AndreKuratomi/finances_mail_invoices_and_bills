import os
import requests
import time

from django.conf import settings
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import render_to_string

from dotenv import load_dotenv

from pathlib import Path

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
                        "receiver_email": "andrekuratomi@gmail.com"
                    }

                    # USERNAME AND EMAIL TO WORK WITH:
                    # data={'competencia_por_ano': "", 'nfe': "", 'nome_do_cliente': "", , 'tipo_de_servico': ""}
                    
                    # serializer = EmailSerializer(data)
                    # # print(serializer)
                    # if not serializer.is_valid():
                    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Extract info from PDF:
                    path = Path("./robot_sharepoint/attachments/")
                    print(path)
                    tables_path_content = list(path.iterdir())

                    for file in tables_path_content:
                        print(file)
                        stringfied = str(file)
                        if stringfied.startswith("NFE"):
                            stringfied = "NFE 17779 FIXO - ECOPORTO.pdf" 
                            specific_char_1 = "-"
                            specific_char_2 = "."
                            index_hifen = stringfied.rfind(specific_char_1)
                            index_dot = stringfied.rfind(specific_char_2)

                            tipo_de_servico = stringfied[10:index_hifen-1]
                            nome_do_cliente = stringfied[index_hifen+2:index_dot]

                    table_template = ""
                    if tables_path_content.count(3):
                        table_template = "table_template_boleto.html"
                    else:
                        table_template = "table_template_deposito.html"

                    print(table_template)

                    # Insert table to mail body:
                    mail_content = render_to_string(
                        table_template, {
                            # 'competencia_por_ano': row_data['competencia_por_ano'], 
                            'nfe': row_data['nfe'], 
                            'nome_do_cliente': nome_do_cliente, 
                            'receiver_email': row_data['receiver_email'], 
                            'tipo_de_servico': tipo_de_servico
                        }
                        #  , using='ISO-8859-1'
                    )
                    # print(mail_content)
                    time.sleep(2)  # wait for file to be created

                    ipdb.set_trace()
                    email = EmailMessage(
                        "Nota Fiscal Eletrônica - J&C Faturamento - {a1}  {a2}  ( {a3} )  NF -  -  - {a4}"
                        .format(
                            # a1=row_data['tipo_de_servico'], 
                            # a2=row_data['competencia_por_ano'], 
                            # a3=row_data['nome_do_cliente'], 
                            a4=row_data['nfe']
                        ),
                        # "Envio tabela  {a1} - Novelis".format(a1=row_data['receiver_name']),
                        "",
                        "{}".format(host_email), 
                        [row_data['receiver_email']], 
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
        
