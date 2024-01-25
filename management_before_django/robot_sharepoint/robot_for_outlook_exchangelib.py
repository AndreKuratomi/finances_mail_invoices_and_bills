import os

from dotenv import load_dotenv
from exchangelib import Account, Configuration, Credentials, DELEGATE, HTMLBody, Message
# from exchangelib import Credentials

import ipdb

load_dotenv()

# ENVS:
# Keys for login:
username = os.getenv("USER_OUTLOOK")
password = os.getenv("USER_OUTLOOK_PASSWORD")

def func_for_search(username, password, cnpj, nfe, razao_social, valor_liquido):
    print(username)
    credentials = Credentials(username, password)
    print(credentials)

    config = Configuration(server='outlook.office365.com', credentials=credentials)
    print(config)

    account = Account(username, credentials=credentials, autodiscover=False, config=config, access_type=DELEGATE)
    print(account)
    # target_subject = 'Subject of the email you are looking for'
    target_emails = account.inbox.filter(subject=nfe)
    print(target_emails)
    ipdb.set_trace()

    # # Create a new email message
    # email = Message(account, folder="Sent Items")
    # email.subject = subject
    # email.body = HTMLBody(body)
    # email.to_recipients = [to_email]

    # # Attach files
    # for attachment_path in attachments:
    #     with open(attachment_path, "rb") as file:
    #         content = file.read()
    #         email.attach(content, name=attachment_path)

# def func_for_search(username: str, password: str, cnpj: str, nfe: str, razao_social: str, valor_liquido: str):
#     """Comment"""
#     # credentials = 
#     outlook_app = "Outlook.Application"
#     outlook_app = "Outlook.Application"
#     namespace = outlook_app.GetNamespace("MAPI")

#     namespace.Logon(username, password, True, False)

#     inbox = namespace.GetDefaultFolder(6)
#     # inbox = outlook_app.CreateItem(0)

#     inbox.Display()

#     print(inbox)
#     print("Logged in into:", username)
#     # pass    

func_for_search(username, password, "00.000.000/0000-00", "00000", "TESTE LTDA", "R$ 20.000,00")
# func_for_search("notafiscal@jcgestaoderiscos.com.br", "Tup27768", "00.000.000/0000-00", "00000", "TESTE LTDA", "R$ 20.000,00")
