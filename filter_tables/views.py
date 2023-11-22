from django.conf import settings
from django.core.mail import EmailMessage, mail_admins, send_mail
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TableName
from .serializers import EmailSerializer

import ipdb


table_data = TableName.objects.all()
# print(table_data)

class SendEmailView(APIView):
    def post(self, request):

        serializer = EmailSerializer(data=request.data)
        # print(request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Creating table from model:
        table_html = "<table>"
        table_html += "<tr>"
        for field1 in TableName._meta.fields:
            if field1.verbose_name == 'index':
                continue
            else:
            # table_html += "<th class=\"head\">{}</th>".format(field1.verbose_name)
                table_html += "<th>{}</th>".format(field1.verbose_name)
        table_html += "</tr>"
        # ipdb.set_trace()
        
        for instance in table_data:
            table_html += "<tr>"
            for field2 in instance._meta.fields:
                table_html += "<td>{}</td>".format(getattr(instance, field2.name))
            table_html += "</tr>"
        
        table_html += "</table>"

        table_to_mail = render_to_string('filter_tables/table_template.html', {'receiver_name': request.data['receiver_name'], 'table_data': table_html})
        # print(table_to_mail)


        send_mail(
            "Envio tabela  {a1} - Novelis".format(a1=request.data['receiver_name']),
            "",
            "suporte.novelis.prototipo@gmail.com", 
            [request.data['receiver_email']], 
            fail_silently=False,
            html_message=table_to_mail
            )


        return Response({"message": "Email successfully sent"}, status=status.HTTP_200_OK)

# send_email("Andre", "andrekuratomi@gmail.com")
