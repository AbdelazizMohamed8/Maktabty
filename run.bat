@echo off
echo ≡ Starting Maktabty Flask Project...
echo.

REM Activate virtual environment if exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo Running local server...
python -m pip install flask flask_sqlalchemy flask_bcrypt flask_login >nul 2>&1

python Maktabty.py
pause
