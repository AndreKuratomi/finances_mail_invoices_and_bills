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

                    row_data = {"cnpj": cnpj, "nfe": nfe, "razao_social": razao_social, "valor_liquido": valor_liquido, "vencimento": vencimento}

                    # TAKING INPUT IDS WITH SELENIUM ROBOT:
                    input_ids = recursive_robot(username, sharepoint_url)
                    print(input_ids)
                    
                    # PLACING TABLE TO WORK WITH WITH SELENIUM ROBOT:
                    robot_for_sharepoint(username, password, input_ids["user_input_id"], input_ids["password_input_id"], sharepoint_url, download_directory, "02390435000115", "17779")
                    # robot_for_sharepoint(username, password, input_ids["user_input_id"], input_ids["password_input_id"], sharepoint_url, download_directory, row_data["cnpj"], row_data["nfe"])

                    print("here i am!")
                    SendEmailView(APIView)
                    # response = requests.post("<my_powerautomate_http_endpoint>", json=row_data)

                    # if response.status_code == 200:
                    #     print("Flow working!")
                    # else:
                    #     print(f"Error! Status code {response.status_code}")
                    # counter += 1


                    # print("Email successfully sent! Check inbox.")

            return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)
  
        except:
            return Exception({"error": "Something went wrong! Contact the dev!"})

class SendEmailView(APIView):
    def post(self):
        try: 
            # USERNAME AND EMAIL TO WORK WITH:
            data={'competencia/ano': "", 'nfe': "", 'nome_do_cliente': "", 'receiver_email': "andrekuratomi@gmail.com", 'tipo_de_servico': ""}
            
            # serializer = EmailSerializer(data)
            # # print(serializer)
            # if not serializer.is_valid():
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Insert table to mail body:
            mail_content = render_to_string('table_template.html', {'competencia/ano': data['competencia/ano'], 'nfe': data['nfe'], 'nome_do_cliente': data['nome_do_cliente'], 'receiver_email': data['receiver_email'], 'tipo_de_servico': data['tipo_de_servico']}
                                            #  , using='ISO-8859-1'
                                            )
            # print(mail_content)
            time.sleep(2)  # wait for file to be created

            email = EmailMessage(
                "Nota Fiscal Eletrônica - J&C Faturamento - {a1}  {a2}  ( {a3} )  NF -  -  - {a4}".format(a1=data['tipo_de_servico'], a2=data['competencia/ano'], a3=data['nome_do_cliente'], a4=data['nfe']),
                # "Envio tabela  {a1} - Novelis".format(a1=data['receiver_name']),
                "",
                "{}".format(host_email), 
                [data['receiver_email']], 
                fail_silently=False,
                html_message=mail_content
            )
            
            # Attach files to email:
            path = Path("../../robot_sharepoint/attachments/")
            tables_path_content = list(path.iterdir())

            for file in tables_path_content:
                print(file)
                str(file)
                email.attach_file(file)

            email.send()

            print("Email successfully sent! Check inbox.")

            return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)
        
        except:
            return Exception({"error": "Something went wrong! Contact the dev!"})
