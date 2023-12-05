import os

from django.conf import settings
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import render_to_string

from dotenv import load_dotenv

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TableName
from .serializers import EmailSerializer

import ipdb

load_dotenv()

host_email = os.getenv("EMAIL_HOST_USER")

# Table to work with:
table_data = TableName.objects.all()


class SendEmailView(APIView):
    def post(self, request):

        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Creating table from model:
        table_html = "<table>"
        table_html += "<tr>"
        
        # <TH>s:
        for field1 in TableName._meta.fields:
            if field1.verbose_name == 'index':
                continue
            else:
                table_html += "<th>{}</th>".format(str(field1.verbose_name).upper())
        table_html += "</tr>"
        
        # <TD>s:
        for instance in table_data:
            table_html += "<tr>"
            counter = 0
            for field2 in instance._meta.fields:
                if counter == 0 or counter % 16 == 0:
                    counter += 1
                    continue
                else:
                    table_html += "<td>{}</td>".format(getattr(instance, field2.name))
                    counter += 1
            table_html += "</tr>"
        
        table_html += "</table>"

        # Insert table to mail body:
        table_to_mail = render_to_string('filter_tables/table_template.html', {'receiver_name': request.data['receiver_name'], 'table_data': table_html})


        send_mail(
            "Envio tabela  {a1} - Novelis".format(a1=request.data['receiver_name']),
            "",
            "{}".format(host_email), 
            [request.data['receiver_email']], 
            fail_silently=False,
            html_message=table_to_mail
        )


        return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)
