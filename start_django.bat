@echo off
REM Quick start script for Django + HTMX frontend

echo ======================================================================
echo BITE-PIPER Django + HTMX Server
echo ======================================================================
echo.

cd src

echo Checking for Django installation...
python -c "import django" 2>nul
if errorlevel 1 (
    echo Django not found! Installing...
    pip install django
    echo.
)

echo Starting Django development server...
echo.
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo ======================================================================
echo.

python manage.py runserver

pause
