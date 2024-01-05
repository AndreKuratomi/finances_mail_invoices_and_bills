chcp 65001 > nul

@echo off

REM Entering directories...

:: echo CurrentDirectory: %CD%
:: echo whatIsThis: %UserProfile%

cd "C:\Users\andre.kuratomi\OneDrive - JC Gestao de Riscos\Área de Trabalho\tables_to_db_mail\tables_to_db_and_mail\"


REM Activating virtual environment...

call ".\env\Scripts\activate"

cd ".\management_before_django\table_management_scripts\"

IF %ERRORLEVEL% NEQ 0 ( 
	echo Failed to enter directories. 
	goto :eof 
)


REM Running script...

py tables_to_db.py 

IF %ERRORLEVEL% NEQ 0 ( 
	echo Script execution failed. 
	goto :eof 
)

echo Script executed successfully.
pause
