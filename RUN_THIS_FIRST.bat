@echo off
REM Check if Python is installed
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Please install Python from https://www.python.org/downloads/.
    exit /b
)

REM Install pip if not installed
python -m ensurepip --upgrade

REM Install libraries
echo Installing required libraries...
pip install -r requirements.txt