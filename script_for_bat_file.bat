chcp 65001 > nul

@echo off

REM Entering directories...

:: echo CurrentDirectory: %CD%
:: echo whatIsThis: %UserProfile%

cd "C:\Users\andre.kuratomi\Desktop\projetos\finances_tables_to_db_and_mail\"


REM Activating virtual environment...

call ".\env\Scripts\activate"

REM Running script...

py run_everything_here.py 

IF %ERRORLEVEL% NEQ 0 ( 
	echo Script execution failed. 
	goto :eof 
)

echo Script executed successfully.
pause
