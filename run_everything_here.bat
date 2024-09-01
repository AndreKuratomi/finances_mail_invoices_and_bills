chcp 65001 > nul

@echo off

REM Entering directories...

:: echo CurrentDirectory: %CD%
:: echo whatIsThis: %UserProfile%

cd "C:\Users\andre.kuratomi\Desktop\projetos\finances_mail_invoices_and_bills\"


REM Activating virtual evironment... OBS: INSTALL THE DEPENDENCIES BEFORE RUNNING IT!!

call ".\venv\Scripts\activate"

REM Running application...

py run_everything_here.py 


IF %ERRORLEVEL% NEQ 0 ( 
	echo THE APPLICATION EXECUTION FAILED! 
	goto :eof 
)

echo APPLICATION EXECUTED SUCCESFULLY!
pause
