# finances_table_to_db_and_mail

- [Traduções](#traduções)
- [Sobre](#sobre)
- [Descrição](#descrição)
- [Instalação](#instalação)
- [Comandos](#comandos)
- [Referências](#referências)

<br>

## Traduções

- [Português brasileiro / Brazilian portuguese](/.multilingual_readmes/README.pt-br.md)
- [Inglês / English](https://github.com/AndreKuratomi/finances_tables_to_db_and_mail)

<br>

## Sobre

A aplicação <strong>finances_table_to_db_and_mail</strong> se propõe a buscar e baixar no sharepoint por arquivos de faturamento para serem anexados e enviados por email a partir de uma planilha fornecida. Junto com isso é enviado para o sharepoint relatório descrevendo casos bem-sucedidos e mal-sucedidos de envio no processo.

Esta aplicação utiliza o framework <strong>[Django](https://www.djangoproject.com/)</strong>, as bibliotecas <strong>[OpenPyXl](https://openpyxl.readthedocs.io/en/stable/tutorial.html)</strong>, <strong>[Pandas](https://pandas.pydata.org/docs/)</strong> e <strong>[Selenium](https://pypi.org/project/selenium/)</strong> e o banco de dados <strong>[SQLite3](https://docs.python.org/3/library/sqlite3.html)</strong>.

<br>

## Descrição

<b>finances_table_to_db_and_mail</b> é uma automatização do processo de análise de planilha, busca no sharepoint por arquivos por período, CNPJ e número da NFE. 

<h3>Processo resumido</h3>

A aplicação inteira é acionada no diretório raiz no script './run_everything_here.py' ou pelo arquivo .bat 'script_for_bat_file.bat'

Ela inicialmente insere na planilha fornecida em 'raw_table/' uma coluna 'STATUS' usando <b>OpenPyXl</b> e a salva em 'edited_table/', depois transforma a planilha editada em um dataframe usando <b>Pandas</b> e com isso filtra por determinadas colunas e insere uma nova coluna 'ID'. 

Manipulado o dataframe ele é inserido em um banco de dados <b>SQLite3</b> em 'db/' e transformado em uma model do <b>Django</b> usando o comando <strong>inspectdb</strong>. Isto possibilita o uso do framework  <b>Django</b> para utilizar o container <b>EmailMessage</b> para anexar e enviar os emails para clientes. Para cada email enviado a planilha é editada na coluna 'STATUS'.

<h3>Planilha</h3>

A aplicação iniciamente busca por uma planilha presente no diretório './finances_table_to_db_and_mail/management_before_django/raw_table'. Se encontrada a aplicação segue com o processo acima e busca de anexos. Senão, a aplicação usa <b>selenium</b> para buscar pela planilha no sharepoint.

<h3>Anexos</h3>

Para obter os anexos, a aplicação utiliza a biblioteca <b>Selenium</b> para buscar no <b>sharepoint</b> pelos anexos por CNPJ e NFE. 
Se encontrados, os anexos são baixados um por um no diretório './finances_table_to_db_and_mail/robot_sharepoint/attachments/'. Os anexos são lidos em './finances_table_to_db_and_mail/dj_project/filter_tables/views.py' e conforme o conjunto dos anexos é escolhido o template para compor o corpo do email em './finances_table_to_db_and_mail/dj_project/filter_tables/templates/'.

Quando não encontrados, a aplicação segue buscando pelos próximos anexos.

<h3>Relatórios</h3>

Os anexos encontrados e não encontrados são registrados em arquivos de texto criados em './finances_table_to_db_and_mail/robot_sharepoint/reports/'. Quando o processo é finalizado ou interrompido é automaticamente criado um terceiro arquivo de texto que junta os dois anteriores. Este terceiro arquivo é enviado para o sharepoint para servir de registro para cada operação finalizada ou não.

<h3>Estudos de caso</h3>

Segue uma listagem resumida de como a aplicação se comporta por situação:

ERROS:

    1. Processo interrompido (cai a luz, máquina sem internet, usuário fecha terminal sem querer):
        Procedimento:
            Fim do processo.
        Ao retomar:
            Base de dados se mantém como estava;
            Tabela baixada deve se manter;
            Tabela editada deve se manter
            Relatório enviados se mantém;
            Relatório não enviados apagado;
            Relatório final recriado.

    2. Processo interrompido (erro interno ou interrupção voluntária do processo no terminal (ex: fim de expediente)):
        Procedimento:
            Relatório final (enviados e não encontrados) enviado sharepoint;
            Fim do processo.
        Ao retomar:
            Base de dados se mantém como estava;
            Tabela baixada deve se manter como estava;
            Tabela editada deve se manter como estava;
            Relatório enviados se mantém;
            Relatório não enviados apagado;
            Relatório final recriado.

IDEAL:

    3. Processo finalizado durante período faturamentos (novos faturamentos virão):
        Procedimento:
            Relatório final (enviados e não encontrados) enviado sharepoint;
            Apagar tabela baixada;
            Manter tabela editada;
            Fim do processo.
        Ao retomar:
            Base de dados se mantém;
            Tabela baixada deve se manter como estava;
            Tabela editada deve se manter como estava;
            Relatório enviados se mantém;
            Relatório não enviados apagado;
            Relatório final recriado.

    4. Processo finalizado (período faturamentos encerrado - todos os faturamentos enviados OU VIRADA DO MÊS*):
        Procedimento:
            Apagar tabelas;
            Apagar relatórios;
            Fim do processo.
        Ao retomar:
            Baixar base de dados;
            Tabela baixada deve ser criada;
            Tabela editada deve ser criada;
            Relatório enviados deve ser criada;
            Relatório não enviados deve ser criada;
            Relatório final recriado.

<!-- <h3>Fluxograma</h3>  ? -->

<br>

## Instalação

<h3>0. Primeiramente, é necessário já ter instalado na própria máquina:</h3>

- O versionador de codigo <b>[Git](https://git-scm.com/downloads)</b>.

- A linguagem de programação <b>[Python](https://www.python.org/downloads/)</b>.

- Um <b>editor de código</b>, conhecido também como <b>IDE</b>. Por exemplo, o <b>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</b>.

- Uma <b>ferramenta cliente de API REST</b>. Por exemplo, o <b>[Insomnia](https://insomnia.rest/download)</b> ou o <b>[Postman](https://www.postman.com/product/rest-client/)</b>.

- <p> E versionar o diretório escolhido para receber o clone da aplicação:</p>

```
git init
```
<br>

<h3>1. Fazer o clone do reposítório <span>python_django_tables_filter_mail</span> na sua máquina pelo terminal do computador ou pelo do IDE:</h3>

```
git clone https://github.com/AndreKuratomi/finances_tables_to_db_and_mail.git
```

WINDOWS:

Obs: Caso apareca algum erro semelhante a este: 

```
unable to access 'https://github.com/AndreKuratomi/finances_tables_to_db_and_mail.git': SSL certificate problem: self-signed certificate in certificate chain
```

Configure o git para desabilitar a certificação SSL:

```
git config --global http.sslVerify "false"
```

<p>Entrar na pasta criada:</p>

```
cd finances_tables_to_db_and_mail
```
<br>

<h3>2. Após feito o clone do repositório, instalar:</h3>

<h4>O ambiente virtual e atualizar suas dependências com o seguinte comando:</h4>

LINUX:
```
python3 -m venv venv --upgrade-deps
```

WINDOWS:
```
py -m venv env
```

<h4>Ative o seu ambiente virtual com o comando:</h4>

LINUX:
```
source/venv/bin/activate
```

WINDOWS:

No sistema operacional Windows é necessário antes configurar o Execution Policy do PowerShell:

```
Get-ExecutionPolicy # para verificar o tipo de política de execução
Set-ExecutionPolicy RemoteSigned # para alterar o tipo de política se o comando acima mostrar 'Restricted'
```
Obs: Eventualmente, pode ser necessário abrir o PowerShell como administrador.

```
.\env\Scripts\activate
```


<h4>Instalar suas dependências:</h4>

```
pip install -r requirements.txt
```

WINDOWS:

Caso seja retornado algum erro semelhante a este:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\Users\\andre.kuratomi\\OneDrive - JC Gestao de Riscos\\Área de Trabalho\\tables_to_db_mail_for_finances\\tables_to_db_and_mail_finances\\env\\Lib\\site-packages\\jedi\\third_party\\django-stubs\\django-stubs\\contrib\\contenttypes\\management\\commands\\remove_stale_contenttypes.pyi'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled. You can find information on how to enable this at https://pip.pypa.io/warnings/enable-long-paths
```

Rode no cmd como adminstrador o seguinte comando:

```
reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```
<br>

<h3>3. E rodar a aplicação:</h3>

```
code .
```
<br>

<h3>4. Create <b>.env</b> file:</h3>

./
```
touch .env
```

Dentro dele precisamos definir nossas variáveis de ambiente tendo como referência o arquivo <b>.env.example</b>:

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

Obs: As informações contidas no arquivo .env não devem ser compartilhadas. O arquivo já consta no .gitignore para não ser subido no repositório.

<br>

## Comandos

Para todos os procedimentos necessários para a aplicação trabalhar basta rodar apenas o comando abaixo:

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

## Referências

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
