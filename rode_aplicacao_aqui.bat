chcp 65001 > nul

@echo off

REM Entering directories...

:: echo CurrentDirectory: %CD%
:: echo whatIsThis: %UserProfile%

cd "C:\Users\andre.kuratomi\Desktop\projetos\notas_fiscais_financeiro\"


REM Ativando ambiente virtual... OBS: INSTALAR AS DEPENDÊNCIAS ANTES DE RODAR!

call ".\env\Scripts\activate"

REM Rodando aplicação...

py rode_tudo_aqui.py 


IF %ERRORLEVEL% NEQ 0 ( 
	echo EXECUCAO DA APLICACAO FALHOU! 
	goto :eof 
)

echo APLICACAO EXECUTADA COM SUCESSO!
pause
