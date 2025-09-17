@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

echo ----------------------------------------
echo Python and pip Setup Checker
echo ----------------------------------------

set "PYTHON_PATH="
set "PIP_PATH="

:: --- Try registry (real Python installs) ---
for %%K in ("HKCU\Software\Python\PythonCore" "HKLM\Software\Python\PythonCore") do (
    for /f "tokens=1" %%V in ('reg query %%K 2^>nul ^| findstr /R "\\[0-9][0-9.]*$"') do (
        for /f "tokens=2*" %%I in ('reg query "%%V\InstallPath" /ve 2^>nul ^| findstr /R "REG_SZ"') do (
            if exist "%%J\python.exe" (
                set "PYTHON_PATH=%%J\python.exe"
                goto :check_pip
            )
        )
    )
)

:: --- Try PATH search (python, python3, py) but skip Store version ---
for %%P in (python python3 py) do (
    for /f "delims=" %%A in ('where %%P 2^>nul') do (
        echo %%A | find /i "WindowsApps" >nul
        if !errorlevel! == 0 (
            rem skip
        ) else (
            echo %%A | find /i "PythonSoftwareFoundation.Python.3" >nul
            if !errorlevel! == 0 (
                rem skip
            ) else (
                set "PYTHON_PATH=%%A"
                goto :check_pip
            )
        )
    )
)

:check_pip
if not defined PYTHON_PATH (
    echo ERROR: No valid Python installation found.
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Found Python at: %PYTHON_PATH%
echo.

:: --- Try to find pip.exe directly ---
for /f "delims=" %%A in ('where pip 2^>nul') do (
    set "PIP_PATH=%%A"
    goto :found_pip_exe
)

:: --- Fall back to python -m pip ---
"%PYTHON_PATH%" -m pip --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip not available through this Python.
    echo Please install pip or use Python from python.org.
    echo.
    pause
    exit /b 1
)
set "PIP_PATH=%PYTHON_PATH% -m pip"
goto :install_reqs

:found_pip_exe
echo Found pip at: %PIP_PATH%
echo.

:install_reqs
echo Installing Python libraries from requirements.txt...
%PIP_PATH% install --upgrade pip
%PIP_PATH% install -r requirements.txt

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
