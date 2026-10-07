@echo off
setlocal

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing packages...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.

pause
