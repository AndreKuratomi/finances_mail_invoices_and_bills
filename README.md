## python_django_tables_filter_mail

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Comandos](#Comandos)
- [Documentação](#documentação)

<br>

# Sobre

<p>A API <b>python_django_tables_filter_mail</b> se propõe a manipular planilhas, filtra-las e envia-las por email.

Esta aplicação utiliza o framework <b>Django</b> e o banco de dados <b>SQLite3</b>.</p>
<br>

# Instalação

<h5>0. Primeiramente, é necessário já ter instalado na própria máquina:</h5>

- O versionador de codigo <b>[Git](https://git-scm.com/downloads)</b>.

- A linguagem de programacao <b>[Python](https://www.python.org/downloads/)</b>.

- Um <b>editor de código</b>, conhecido também como <b>IDE</b>. Por exemplo, o <b>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</b>.

- Uma <b>ferramenta cliente de API REST</b>. Por exemplo, o <b>[Insomnia](https://insomnia.rest/download)</b> ou o <b>[Postman](https://www.postman.com/product/rest-client/)</b>.

- <p> E versionar o diretório escolhido para receber o clone da aplicação:</p>

```
git init
```

<br>
<h5>1. Fazer o clone do reposítório <span>python_django_tables_filter_mail</span> na sua máquina pelo terminal do computador ou pelo do IDE:</h5>

```
git clone https://github.com/AndreKuratomi/tables_to_db_and_mail.git
```

Windows:

Obs: Caso apareca algum erro semelhante a este: 

```
unable to access 'https://github.com/AndreKuratomi/tables_to_db_and_mail.git/': SSL certificate problem: self-signed certificate in certificate chain
```

Configure o git para desabilitar a certificação SSL:

```
git config --global http.sslVerify "false"
```

<p>Entrar na pasta criada:</p>

```
cd python_django_tables_filter_mail
```

Após feito o clone do repositório, instalar:

<h6>O ambiente virtual e atualizar suas dependências com o seguinte comando:</h6>

Linux:
```
python3 -m venv venv --upgrade-deps
```

Windows:
```
py -m venv env
```
<br>
<h6>Ative o seu ambiente virtual com o comando:</h6>

Linux:
```
source/venv/bin/activate
```

Windows:

No sistema operacional Windows é necessário antes configurar o Execution Policy do PowerShell:

```
Get-ExecutionPolicy # para verificar o tipo de política de execução
Set-ExecutionPolicy RemoteSigned # para alterar o tipo de política se o comando acima mostrar 'Restricted'
```
Obs: Eventualmente, pode ser necessário abrir o PowerShell como administrador.

```
.\env\Scripts\activate
```
<br>
<h6>Instalar suas dependências:</h6>

```
pip install -r requirements.txt
```

<h6>E rodar a aplicação:</h6>

```
code .
```

# Comandos

Para todos os procedimentos necessarios basta rodar apenas o comando abaixot:

./management_before_django/table_management_scripts/

```
python3 tables_to_db.py
```

<br>

# Documentação

Para ter acesso ao descrições detalhes das rotas e seus retornos, conferir documentação completa no link a seguir:

(link)
