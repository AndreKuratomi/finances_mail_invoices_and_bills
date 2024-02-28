## finances_table_to_db_and_mail

- [Translates](#translates)
- [Description](#Description)
- [Instalation](#instalation)
- [Comandos](#Comandos)

<br>

# Translates:

- [English](https://github.com/AndreKuratomi/finances_tables_to_db_and_mail)
- [Português Brasileiro / Brazilian portuguese](/.multilingual_readmes/README.pt-br.md)

<br>

# Description:

<p>The application <b>python_django_tables_filter_mail</b> that manipulates spreadsheets, extracts its lines to look for its content in <strong>sharepoint</strong> folders, downloads it when found and attaches it to emails to send to clients.

This application uses <strong>Python</strong>'s framework <strong>Django</strong>, <strong>Pandas</strong>, <strong>OpenPyXl</strong> and <strong>Selenium</strong> libs and the <strong>SQLite3</strong> database.</p>
<br>

# Instalation:

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
py -m venv env
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

# Commands:

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


