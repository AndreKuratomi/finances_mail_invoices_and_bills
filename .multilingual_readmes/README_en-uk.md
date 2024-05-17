# finances_table_to_db_and_mail

- [Translates](#translates)
- [About](#About)
- [Description](#Description)
- [Instalation](#instalation)
- [Commands](#Commands)
- [References](#references)

<br>

## Translates

- [Português brasileiro / Brazilian portuguese](https://github.com/AndreKuratomi/notas_fiscais_financeiro)
- [Inglês / English](./.multilingual_readmes/README.en-uk.md)

<br>

## About

<p>The application <b>python_django_tables_filter_mail</b> that manipulates spreadsheets, extracts its lines to look for its content in <strong>sharepoint</strong> folders, downloads it when found and attaches it to emails to send to clients.


The application <strong>finances_table_to_db_and_mail</strong> is purposed to search and dowload files from sharepoint to be attached and sent by email from a given spreadsheet. During this process it is also sent to sharepoint a report describing its succesfull ands non-successfull cases.

This application uses <strong>Python</strong>'s framework <strong>[Django](https://www.djangoproject.com/)</strong>, the libs <strong>[OpenPyXl](https://openpyxl.readthedocs.io/en/stable/tutorial.html)</strong>, <strong>[Pandas](https://pandas.pydata.org/docs/)</strong> and <strong>[Selenium](https://pypi.org/project/selenium/)</strong> and the <strong>[SQLite3](https://docs.python.org/3/library/sqlite3.html)</strong> database.

<br>

## Description

<b>finances_table_to_db_and_mail</b> is the automatization of spreadsheet analisys, search on sharepoint for by period, UserID and NFE number. 

<h3>Summary process</h3>

The whole application can be runned at the root directory bu the script './run_everything_here.py' or by the .bat file 'script_for_bat_file.bat'.

It firstly inserts in the given table in 'raw_table/' a 'STATUS' column using <b>OpenPyXl</b> and saves it in 'edited_table/', after that it transforms the edited spreadsheet into a dataframe using <b>Pandas</b> and it is filtered by specific columns and inserts a new column 'ID'. 

After manipulation the dataframe is inserido in a database <b>SQLite3</b> in 'db/' and transformed into a <b>Django</b> model using the command <strong>inspectdb</strong>. This makes <b>Django</b> able to use the container <b>EmailMessage</b> for attachimng and sending emails to clients. 

<h3>Spreadsheet</h3>

The aplication firstly searches for a spreadsheet in the directory './finances_table_to_db_and_mail/management_before_django/raw_table'. if found the aplication follows up looking for attachments. If not, it uses <b>selenium</b> to search for the spreadsheet on sharepoint.

<h3>Attachments</h3>

To obtain them, the application uses the lib <b>Selenium</b> for searching for attachments by CNPJ and NFE on <b>sharepoint</b>. 
If found, they are downloaded one by one on the directory './finances_table_to_db_and_mail/robot_sharepoint/attachments/'. The attachments are read with './finances_table_to_db_and_mail/dj_project/filter_tables/views.py' and according to the attachments amount the appropriate template is chosen for the email body in './finances_table_to_db_and_mail/dj_project/filter_tables/templates/'.

When not found, the application follows up looking for other attachments.

<h3>Reports</h3>

The found and not found attachments are registered in text files at './finances_table_to_db_and_mail/robot_sharepoint/reports/'. When the process is ended or interrupted it is automatically created a a third text file that gathers the first two. This third text file is sent to sharepoint as report of the operaion even if it is not finalized.

<h3>Case studies</h3>

Bellow a resumed list of the application behaviour by case:

ERROR:

    1. Interrupted process (lack of light energy, lack of internet, user closes terminal accidentally):
        Procedure:
            Process finished.
        When restart process:
            Spreadsheet is maintaned;
            Spreadsheet downloaded remains;
            Spreadsheet edited remains;
            Sent elements report remains;
            Not sent elements report deleted;
            Final report recriated.

    2. Interrupted process (internal error or voluntairly interruption of process on terminal (ex: end of working day)):
        Procedure:
            Final report sent to sharepoint;
            Process finished.
        When restart process:
            Spreadsheet is maintaned;
            Downloaded spreadsheet remains;
            Edited spreadsheet remains;
            Sent elements report remains;
            Not sent elements report deleted;
            Final report recriated.

IDEAL:

    3. Process ended durante período faturamentos (will billings will come):
        Procedure:
            Final report sent to sharepoint;
            Delete downloaded spreadsheet;
            Edited spreadsheet remains;
            Process finished.
        When restart process:
            spreadsheet remains;
            Downloaded spreadsheet remains;
            Edited spreadsheet remains;
            Sent elements report remains;
            Not sent elements report deleted;
            Final report recriated.

    4. Process ended (end of billings period - all billings sent OR MONTH TURN*):
        Procedure:
            Apagar Spreadsheets;
            Apagar relatórios;
            Process finished.
        When restart process:
            Download spreadsheet;
            Spreadsheet downloaded is created;
            Spreadsheet edited is created;
            Sent elements report is created;
            Not sent elements report is created;
            Final report recriated.

<br>

## Instalation:

<h3>0. It is first necessary to have instaled the following devices:</h3>

- The code versioning <b>[Git](https://git-scm.com/downloads)</b>.

- A <b>code editor</b>, also known as <b>IDE</b>. For instance, <strong>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</strong>.

- A <b> client API REST </b> program. <strong>[Insomnia](https://insomnia.rest/download)</strong> or <b>[Postman](https://www.postman.com/product/rest-client/)</b>, for instance.

- <p> And versioning your directory to receive the aplication clone:</p>

```
git init
```

<br>
<h3>1. Clone the repository <b>finances_tables_to_db_and_mail</b> by your machine terminal or by the IDE:</h3>

```
git clone https://github.com/AndreKuratomi/finances_tables_to_db_and_mail.git
```

WINDOWS:

Obs: In case of any mistake similar to this one: 

```
unable to access 'https://github.com/AndreKuratomi/finances_tables_to_db_and_mail.git/': SSL certificate problem: self-signed certificate in certificate chain
```

Configure git to disable SSL certification:

```
git config --global http.sslVerify "false"
```

<p>Enter the directory:</p>

```
cd finances_tables_to_db_and_mail
```
<br>

<h3>2. After cloning the repository install:</h3>

<h4>Virtual enviroment and update its dependencies with the following command:</h4>


LINUX:
```
python3 -m venv venv --upgrade-deps
```

WINDOWS:
```
py -m venv venv
```
<br>
<h4>Ativate your virtual enviroment with the command:</h4>

LINUX:
```
source/venv/bin/activate
```

WINDOWS:

On Windows operational system it is necessary to configure the Execution Policy at PowerShell:

```
Get-ExecutionPolicy # to check the Execution policy type
Set-ExecutionPolicy RemoteSigned # to change the type of policy if the command above shows 'Restricted'
```
Obs: It may often be necessary to open PowerShell as administrador for that.

```
.\env\Scripts\activate
```
<br>
<h4>Install its dependencies:</h4>

```
pip install -r requirements.txt
```
<br>


WINDOWS:

In case any error similar to the one bellow be returned:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\Users\\andre.kuratomi\\OneDrive - JC Gestao de Riscos\\Área de Trabalho\\tables_to_db_mail_for_finances\\tables_to_db_and_mail_finances\\env\\Lib\\site-packages\\jedi\\third_party\\django-stubs\\django-stubs\\contrib\\contenttypes\\management\\commands\\remove_stale_contenttypes.pyi'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled. You can find information on how to enable this at https://pip.pypa.io/warnings/enable-long-paths
```

Run cmd as adminstrador with the following command:

```
reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```
<br>

<h3>3. And run the aplication:</h3>

```
code .
```
<br>

<h3>4. Create <b>env</b> file:</h3>

```
touch .env
```


<h3>4. Create <b>.env</b> file:</h3>

./
```
touch .env
```

Inside it we need to put our enviroment variables taking as reference the given file <b>.env.example</b>:

```
# DJANGO:
SECRET_KEY=secret_key

# EMAIL VARIABLES:
EMAIL_HOST_USER=host_email
EMAIL_HOST_PASSWORD=host_password

# SHAREPOINT VARIABLES:
SHAREPOINT_FOR_UPLOAD_URL=sharepoint_for_upload_url
SHAREPOINT_FATURAMENTO_URL=faturamento
SHAREPOINT_MEDICOES_URL=medicoes

DOWNLOAD_DIRECTORY=download_directory
RAW_TABLE_DIRECTORY=raw_table_url
```

Obs: Do not share info from .env file. It is already mentioned in .gitignore for not being pushed to the repo.

<br>

## Commands:

For all the necessary procedures for running the aplication we may only run the command bellow:

./

WINDOWS:
```
py run_everything_here.py
```

LINUX:
```
python3 run_everything_here.py
```

<br>

## References

- [Django](https://www.djangoproject.com/)
- [DjangoMail](https://docs.djangoproject.com/en/4.1/topics/email/)
- [Dotenv](https://www.npmjs.com/package/dotenv)
- [Git](https://git-scm.com/downloads)
- [OpenPyXl](https://openpyxl.readthedocs.io/en/stable/tutorial.html)
- [Pandas](https://pandas.pydata.org/docs/)
- [Python](https://www.python.org/downloads/)
- [Selenium](https://pypi.org/project/selenium/)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Visual Studio Code (VSCode)](https://code.visualstudio.com/)


