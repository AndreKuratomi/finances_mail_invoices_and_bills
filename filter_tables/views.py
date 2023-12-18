import os
import time

from django.conf import settings
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import render_to_string

from dotenv import load_dotenv

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tqdm import tqdm

from .models import TableName
from .serializers import EmailSerializer

import ipdb

load_dotenv()

host_email = os.getenv("EMAIL_HOST_USER")

# Table to work with:
table_data = TableName.objects.all()


class SendEmailView(APIView):
    def post(self):
        try: 
            # print("I`M HERE")

            # USERNAME AND EMAIL TO WORK WITH:
            data={'receiver_name': "Andre", 'receiver_email': "andrekuratomi@gmail.com"}
            
            # serializer = EmailSerializer(data)
            # # print(serializer)
            # if not serializer.is_valid():
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Creating table from model:
            table_html = "<table>"
            table_html += "<tr>"
            
            # <TH>s:
            for field1 in tqdm(TableName._meta.fields, "Filtering table from dataframe..."):
                # print(field1.verbose_name)

                if field1.verbose_name == 'index':
                    # print(field1)
                    continue
                elif field1.verbose_name == 'id':
                    # print(field1.verbose_name)
                    continue
                else:
                    # field_value = getattr
                    table_html += "<th>{}</th>".format(str(field1.verbose_name).upper())
            table_html += "</tr>"
            
            # <TD>s:
            for instance in tqdm(table_data, "Creating table for email body..."):
                table_html += "<tr>"
                counter = 0
                for field2 in instance._meta.fields:
                    # Excluding column 'index' content:
                    if counter == 0 or counter % 16 == 0:
                        counter += 1
                        continue
                    # Excluding column 'ID' content:
                    elif counter == 1 or counter % 17 == 0:
                        counter += 1
                        continue
                    # Ordering datetime from 'year-month-day' to 'day-month-year':
                    elif counter == 10 or counter == 11 or counter % 26 == 0 or counter % 27 == 0:
                        field_value = getattr(instance, field2.name)
                        if field_value == None:
                            # print(field_value)
                            field_value = '-'
                            table_html += "<td>{}</td>".format(field_value)
                            counter += 1
                        else:
                            field_value = getattr(instance, field2.name).strftime('%d-%m-%Y %H:%M:%S')
                            table_html += "<td>{}</td>".format(field_value)
                            counter += 1
                    else:
                        table_html += "<td>{}</td>".format(getattr(instance, field2.name))
                        counter += 1
                table_html += "</tr>"
            
            table_html += "</table>"

            # Insert table to mail body:
            table_to_mail = render_to_string('table_template.html', {'receiver_name': data['receiver_name'], 'table_data': table_html}
                                            #  , using='ISO-8859-1'
                                            )
            # print(table_to_mail)
            time.sleep(2)  # wait for file to be created

            send_mail(
                "Envio tabela  {a1} - Novelis".format(a1=data['receiver_name']),
                "",
                "{}".format(host_email), 
                [data['receiver_email']], 
                fail_silently=False,
                html_message=table_to_mail
            )

            print("Email successfully sent! Check inbox.")

            return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)
        
        except:
            return Exception({"error": "Something went wrong! Contact the dev!"})
