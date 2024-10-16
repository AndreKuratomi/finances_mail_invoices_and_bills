# finances_mail_invoices_and_bills

- [Traduções](#traduções)
- [Sobre](#sobre)
- [Descrição_técnica](#descrição_técnica)
- [Instalação](#instalação)
- [Como_fazer_a_aplicação_funcionar](#como_fazer_a_aplicação_funcionar)
- [Referências](#referências)

<br>

## Traduções

- [🇧🇷 Português brasileiro / Brazilian portuguese](/.multilingual_readmes/README_pt-br.md)
- [🇬🇧 / 🇺🇸 Inglês / English](https://github.com/AndreKuratomi/finances_mail_invoices_and_bills)

<br>

## Sobre

<p>A aplicação <b>finances_mail_invoices_and_bills</b> foi desenvolvida para automatizar o envio mensal de notas fiscais e boletos para os clientes de uma empresa. Ela trabalha com as pastas <strong>sharepoint</strong> fornecidos por ela, elabora emails com anexos baixados e relatórios de envios bem sucedidos e mal sucedidos. 

Esta aplicação é feita para não-desenvolvedores operarem ela e pode ser usada uma ou mais vezes por mês dependendo da demanda. Para esta versão ela é acionada manualmente.

Ela foi originalmente desenvolvida para o SO Windows.

Esta aplicação utiliza o framework <strong>[Django](https://www.djangoproject.com/)</strong>, as bibliotecas <strong>[OpenPyXl](https://openpyxl.readthedocs.io/en/stable/tutorial.html)</strong>, <strong>[Pandas](https://pandas.pydata.org/docs/)</strong> e <strong>[Selenium](https://pypi.org/project/selenium/)</strong> e o banco de dados <strong>[SQLite3](https://docs.python.org/3/library/sqlite3.html)</strong>. Ela também trabalha com bateria de testes com <strong>[Pytest](https://docs.pytest.org/en/stable/)</strong>.

<br>

## Descrição_técnica

<b>finances_mail_invoices_and_bills</b> é uma automatização do processo de análise de planilha, busca no sharepoint por arquivos por período, CNPJ e número da NFE. 

<h3>Processo resumido</h3>

A aplicação inteira é acionada no diretório raiz no script './run_everything_here.py' ou pelo arquivo .bat 'script_for_bat_file.bat'

Ela inicialmente insere na planilha fornecida em 'raw_table/' uma coluna 'STATUS' usando <b>OpenPyXl</b> e a salva em 'edited_table/', depois transforma a planilha editada em um dataframe usando <b>Pandas</b> e com isso filtra por determinadas colunas e insere uma nova coluna 'ID'. 

Manipulado o dataframe ele é inserido em um banco de dados <b>SQLite3</b> em 'db/' e transformado em uma model do <b>Django</b> usando o comando <strong>inspectdb</strong>. Isto possibilita o uso do framework  <b>Django</b> para utilizar o container <b>EmailMessage</b> para anexar e enviar os emails para clientes. Para cada email enviado a planilha é editada na coluna 'STATUS'.

Segue uma descrição mais detalhada das partes:

<h3>Planilha</h3>

A aplicação iniciamente busca por uma planilha presente no seu diretório './finances_table_to_db_and_mail/management_before_django/raw_table'. Se encontrada a aplicação segue com o processo acima em busca de anexos. Senão, a aplicação usa a biblioteca <b>Selenium</b> para buscar pela planilha no <b>sharepoint</b>.

Quando o processo é finalizado a planilha baixada em 'raw_table/' é apagada. Assim, quando o processo for refeito a aplicação buscará por uma nova planilha no <b>sharepoint</b>. Se a planilha recém-baixada estiver atualizada a aplicação ao baixá-la vai comparar ela com a planilha editada de 'edite_table/' e atualizar a editada com o conteúdo novo.

<h3>Anexos</h3>

Para obter os anexos, a aplicação utiliza a biblioteca <b>Selenium</b> para buscar no <b>sharepoint</b> pelos anexos por período, CNPJ e NFE. 
Se encontrados, os anexos são baixados um por um no diretório './finances_table_to_db_and_mail/robot_sharepoint/anexos/'. Os anexos são lidos em './finances_table_to_db_and_mail/dj_project/filter_tables/views.py' e conforme o conjunto dos anexos é escolhido o template para compor o corpo do email em './finances_table_to_db_and_mail/dj_project/filter_tables/templates/'.

Quando não encontrados, a aplicação segue buscando pelos próximos anexos.

<h3>Relatórios</h3>

Os anexos encontrados e não encontrados são registrados em arquivos de texto criados em './finances_table_to_db_and_mail/robot_sharepoint/reports/'. Quando o processo é finalizado ou interrompido (mas não fechado) é automaticamente criado um terceiro arquivo de texto que junta os dois anteriores. Este terceiro arquivo é enviado para o sharepoint para servir de registro para cada envio feito ou não.

<h3>Padronização de arquivos e caminhos sharepoint</h3>

DOWNLOAD PLANILHAS:
    
    Planilha CONTATOS (matr020 - CONTATOS.xlsx):

        Obtida no sharepoint em: Documentos > 02 - FATURAMENTO > 14 - BASE DE DADOS

        Linhas:
            Linha 1a: Títulos das colunas
            Demais linhas: (conteúdo)
        Colunas usadas:
            Coluna E (CNPJ/CPF): dd.ddd.ddd/dddd-dd (Ex: 11.222.333/4444-55) # dígitos com '.', '/' e '-'
            Coluna H (E-Mail): formatação padrão email (Ex: nfe@jcgestaoderiscos.com.br)

    Planilha BASE DE DADOS (finr940.xlsx):
        Obtida no sharepoint em:  Documentos > 02 - FATURAMENTO > 14 - BASE DE ENVIO > ANO {número_ano} > {xx} {nome_mês} # Ex: ANO 2023 > 01 JANEIRO 
            Obs: Tanto ano quanto mês são obtidos dinamicamente na aplicação.

            Linhas:
                Linha 1a: Títulos das colunas
                Demais linhas: (conteúdo)
            Colunas usadas:
                Coluna D (Nome do Cliente): texto
                Coluna E (CNPJ): dddddddddddddd (Ex: 01234567890123) # apenas dígitos
                Coluna G (Numero): 0ddddd (Ex: 012345) # número da NFE iniciada por 0
                Coluna K (Dt Vencto): dd/mm/aaaa (Ex: 28/02/2024) # formatação 'dia-mês-ano'
                Coluna S (Valor Liquido): 00.000,00 (50.000,44) # '.' quando houver milhar e ',' para centavos

DOWNLOAD ANEXOS:

    Obtida no sharepoint em:  01 - MEDIÇÕES > ANO {número_ano} > {xx} {nome_mês} > {CNPJ - nome} > {número_nfe} 
        # Ex: ANO 2023 > 01 JANEIRO > 00111222333444455 - nome > 012345
        Obs: Os valores são obtidos dinamicamente na aplicação.

    Boletos:
        "'NFE' <número da nfe> <tipo de serviço> <competenciaano>.pdf" # considerar os espaços
        Por exemplo: 'NFE 17758 FIXO Dezembro24.pdf'.
    Medições:
        "MEDIÇÃO.xlsx" 
        Por exemplo: 'MEDIÇÃO.xlsx'
    NFEs:
        "BOLETO <número da nfe>.pdf"  # considerar o espaço
        Por exemplo: 'BOLETO 17757.pdf'


UPLOAD RELATÓRIOS:

    Obtida no sharepoint em:  Documentos > 02 - FATURAMENTO > 15 - RELATÓRIOS DE ENVIO > ANO {número_ano} > {xx} {nome_mês} 
    # Ex: ANO 2023 > 01 JANEIRO 
    Obs: Tanto ano quanto mês são obtidos dinamicamente na aplicação.

<h3>Estudos de caso</h3>

Segue uma listagem resumida de como a aplicação se comporta por situação:

ERROS:

    1. Processo interrompido totalmente (falta de luz, falta de internet, ou fechamento da aplicação):
        Procedimento:
            Fim do processo.
        Quando retomado:
            Tabela baixada se mantém como estava;
            Tabela editada idem;
            Relatório 'enviados' idem;
            Relatório 'não enviados' recriado;
            Relatório final idem.

    2.  Processo interrompido parcialmente (erro interno ou interrupção voluntária do processo no terminal (CTRL + C uma única vez)):
        Procedimento:
            Relatório final ('enviados' e 'não enviados') enviado sharepoint;
            Fim do processo.
        Quando retomado:
            Tabela baixada se mantém como estava;
            Tabela editada idem;
            Relatório 'enviados' idem;
            Relatório 'não enviados' recriado;
            Relatório final idem.

IDEAL:

    3. Processo finalizado por tabela baixada (novos faturamentos virão):
        Procedimento:
            Relatório final ('enviados' e 'não enviados') enviado sharepoint;
            Apagar tabela baixada;
            Manter tabela editada;
            Fim do processo.
        Quando retomado:
            Tabela baixada se mantém como estava;
            Tabela editada idem;
            Relatório 'enviados' idem;
            Relatório 'não enviados' recriado;
            Relatório final recriado.

    4. Processo finalizado com todos os faturamentos do mês (virada do mês):
        Procedimento:
            Apagar tabelas;
            Apagar relatórios;
            Tabela baixada criada;
            Tabela editada criada;
            Relatório 'enviados' criado;
            Relatório 'não enviados' criado;
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

<h3>1. Fazer o clone do reposítório <span>finances_mail_invoices_and_bills</span> na sua máquina pelo terminal do computador ou pelo do IDE:</h3>

```
git clone https://github.com/AndreKuratomi/finances_mail_invoices_and_bills.git
```

WINDOWS:

Obs: Caso apareca algum erro semelhante a este: 

```
unable to access 'https://github.com/AndreKuratomi/finances_mail_invoices_and_bills.git': SSL certificate problem: self-signed certificate in certificate chain
```

Configure o git para desabilitar a certificação SSL:

```
git config --global http.sslVerify "false"
```

<p>Entrar na pasta criada:</p>

```
cd finances_mail_invoices_and_bills
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
py -m venv venv --upgrade-deps
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
.\venv\Scripts\activate
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

<h3>4. Criar arquivo <b>.env</b>:</h3>

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
SHAREPOINT_MEASUREMENTS_URL=measurements

DOWNLOAD_DIRECTORY=download_directory
RAW_TABLE_DIRECTORY=raw_table_url
```

Obs: As informações contidas no arquivo .env não devem ser compartilhadas. O arquivo já consta no .gitignore para não ser subido no repositório.

<br>

## Como_fazer_a_aplicação_funcionar

1. INÍCIO DA OPERAÇÃO:

    1.1. Via arquivo .bat:

    Para o usuário leigo basta apenas clicar duas vezes no arquivo rode_aplicacao_aqui.bat*: 

    <figure>
        <img src="./assets/double_click_.bat_file.png" alt="Double-click .bat file" style="">
        <!-- <figcaption style="display: none;">Double-click .bat file</figcaption> -->
    </figure>

    *<b>Obs:</b> Este arquivo rode_aplicacao_aqui.bat pode ser retirado dos arquivos da aplicação e colocado na área de trabalho, por exemplo.

    <br>
    
    1.2. Via IDE:

    Para todos os procedimentos necessários para a aplicação trabalhar basta rodar apenas o comando abaixo:

    ./

    WINDOWS:
    ```
    py rode_tudo_aqui.py
    ```

    LINUX:
    ```
    python3 rode_tudo_aqui.py
    ```
    
<br>
    

2. INTERRUPÇÃO TOTAL DA APLICAÇÃO (SEM ENVIO DE RELATÓRIOS):

    Basta fechar o arquivo rode_aplicacao_aqui.bat ou o IDE.
    
<br>
    

3. INTERRUPÇÃO PARCIAL DA APLICAÇÃO (COM ENVIO DE RELATÓRIO DO QUE FOI FEITO ATÉ A INTERRUPÇÃO.)

    Basta clicar <b>"CTRL + C"</b> UMA ÚNICA VEZ que o programa enviará o relatório automaticamente. Se clicar várias vezes nenhum relatório será enviado.

    <figure>
        <img src="./assets/process_partially_interrupted.png" alt="Double-click .bat file" style="">
        <!-- <figcaption style="display: none;">Double-click .bat file</figcaption> -->
    </figure>

    Ao clicar <b>"CTRL + C"</b> a aplicação mostrará a imagem 'ELABORANDO RELATÓRIO FINAL E ENVIANDO'. Aí é só aguardar aparecer 'PROCESSO ENCERRADO. CHECAR RELATÓRIOS.' para ter certeza de que o processo foi finalizado.
<br>

4. Para a primeira operação do mês:

    Antes de rodar a aplicação pela primeira vez no mês (para os faturamentos do mês) é preciso manualmente apagar na aplicação o arquivo <b>DELETE_ME_BEFORE_FIRST_MONTH_OPERATION</b>.

    <figure>
        <img src="./assets/ME_APAGUE.png" alt="DELETE_ME_BEFORE_FIRST_MONTH_OPERATION">
        <!-- <figcaption style="display: none;">DELETE_ME_BEFORE_FIRST_MONTH_OPERATION</figcaption> -->
    </figure>

    Só isso já fará a aplicação apagar o que ela contém do mês anterior e buscar conteúdo novo.


<br>

## Referências

- [Django](https://www.djangoproject.com/)
- [DjangoMail](https://docs.djangoproject.com/en/4.1/topics/email/)
- [Dotenv](https://www.npmjs.com/package/dotenv)
- [Git](https://git-scm.com/downloads)
- [OpenPyXl](https://openpyxl.readthedocs.io/en/stable/tutorial.html)
- [Pandas](https://pandas.pydata.org/docs/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [Python](https://www.python.org/downloads/)
- [Selenium](https://pypi.org/project/selenium/)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Visual Studio Code (VSCode)](https://code.visualstudio.com/)

