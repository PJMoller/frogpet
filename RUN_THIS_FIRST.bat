@echo off
setlocal ENABLEEXTENSIONS

echo ----------------------------------------
echo Python and pip Setup Checker
echo ----------------------------------------

:: Temporarily disable Windows Store redirect by checking what 'where python' returns
where python > "%TEMP%\python_path.txt" 2>&1

setlocal enabledelayedexpansion
set "PYTHON_PATH="
for /f "usebackq delims=" %%A in ("%TEMP%\python_path.txt") do (
    set "line=%%A"
    :: Check if line contains 'python.exe' but not WindowsApps (the store redirect folder)
    echo !line! | find /i "python.exe" >nul
    if !errorlevel! == 0 (
        echo !line! | find /i "WindowsApps" >nul
        if !errorlevel! NEQ 0 (
            set "PYTHON_PATH=!line!"
            goto :found_python
        )
    )
)

:: If no valid python.exe found
echo ERROR: Python executable not found or points to Windows Store app.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to add Python to your system PATH.
echo.
pause
exit /b 1

:found_python
echo Found Python at: %PYTHON_PATH%
echo.

:: Check pip availability
"%PYTHON_PATH%" -m pip --version >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip not available through Python.
    echo Try running: python -m ensurepip --upgrade
    echo Or reinstall Python with pip support.
    echo.
    pause
    exit /b 1
)

:: Install required libraries
echo Installing Python libraries from requirements.txt...
"%PYTHON_PATH%" -m pip install --upgrade pip
"%PYTHON_PATH%" -m pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install required libraries.
    echo Please check your requirements.txt and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo All requirements successfully installed.
pause
exit /b 0
