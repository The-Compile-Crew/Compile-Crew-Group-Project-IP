@echo off
REM run_server.bat — start Flask in a new terminal and open browser to the app root
REM Usage: double-click this file or run it from cmd in the project root.










start "" "http://127.0.0.1:5000/"timeout /t 3 /nobreak >nulif exist "%CD%\venv\Scripts\activate.bat" (
    start "Flask Server" cmd /k "cd /d %CD% && call venv\Scripts\activate.bat && set FLASK_APP=%FLASK_APP% && set FLASK_ENV=%FLASK_ENV% && flask run --host=127.0.0.1 --port=5000"
) else (
    start "Flask Server" cmd /k "cd /d %CD% && set FLASK_APP=%FLASK_APP% && set FLASK_ENV=%FLASK_ENV% && flask run --host=127.0.0.1 --port=5000"
)

:: Wait a short moment then open the browser to the root URL
:: If virtualenv activation script exists, use it in the new window; otherwise start flask directly.set FLASK_ENV=developmentset FLASK_APP=App.views.wsgi
:: Set Flask env varscd /d "%~dp0":: Ensure we run from the script directory (project root)