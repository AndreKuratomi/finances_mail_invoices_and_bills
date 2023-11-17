from django.conf import settings
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.response import Response

from .models import TableName

import ipdb


table_data = TableName.objects.all()
# print(table_data)

def send_email(receiver_name, receiver_mail, table):

    table_to_mail = render_to_string('filter_tables/table_template.html', {'receiver_name': receiver_name, 'table_data': table})
    # print(table_to_mail)
    # ipdb.set_trace()


    send_mail(
        "Envio tabela  {a1} - Novelis".format(a1=receiver_name),
        "",
        "suporte.novelis@gmail.com", 
        [receiver_mail], 
        fail_silently=False,
        html_message=table_to_mail
        )


    return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)

send_email("Andre", "andrekuratomi@gmail.com", table_data)