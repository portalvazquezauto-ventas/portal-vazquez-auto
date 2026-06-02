@echo off
cd /d "%~dp0"
echo Iniciando Portal Vazquez Auto...
echo. | python -m streamlit run app.py
pause
