## vba_python_django

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Comandos](#Comandos)
- [Documentação](#documentação)

<br>

# Sobre

<p>A API <b>vba_python_django</b> se propõe a manipular planilhas, filtra-las e envia-las por email.

Esta aplicação utiliza o framework <b>Django</b> e o banco de dados <b>SQLite3</b>.</p>
<br>

# Instalação

<h5>0. Primeiramente, é necessário já ter instalado na própria máquina:</h5>

- Um <b>editor de código</b>, conhecido também como <b>IDE</b>. Por exemplo, o <b>[Visual Studio Code (VSCode)](https://code.visualstudio.com/)</b>.

- Uma <b>ferramenta cliente de API REST</b>. Por exemplo, o <b>[Insomnia](https://insomnia.rest/download)</b> ou o <b>[Postman](https://www.postman.com/product/rest-client/)</b>.

- <p> E versionar o diretório para receber o clone da aplicação:</p>

```
git init
```

<br>
<h5>1. Fazer o clone do reposítório <span>KenzieDoc</span> na sua máquina pelo terminal do computador ou pelo do IDE:</h5>

```
git clone https://github.com/AndreKuratomi/vba_python_django.git
```

<p>Entrar na pasta criada:</p>

```
cd vba_python_django
```

Após feito o clone do repositório KenzieDoc, instalar:

O ambiente virtual e atualizar suas dependências com o seguinte comando:

```
python -m venv venv --upgrade-deps
```

Ative o seu ambiente virtual com o comando:

```
source/venv/bin/activate
```

Instalar suas dependências:

```
pip install -r requirements.txt
```

E rodar a aplicação:

```
code .
```

# Comandos

Insert table to database:
management/commands/tables_to_db.py
```
python3 tables_to_db.py
```

Create model from db content:
./
```
python3 manage.py inspectdb > filter_tables/models.py
```

Send email (?):
filter_tables/
```
python3 views.py
```



# Documentação

Para ter acesso ao descrições detalhes das rotas e seus retornos, conferir documentação completa no link a seguir:

(link)