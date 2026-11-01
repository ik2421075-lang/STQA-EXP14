@echo off
title COVID-19 Portal ^& Automated Selenium QA Lab
cd /d "%~dp0"

echo ====================================================================
echo   COVID-19 INFORMATION PORTAL ^& SELENIUM QA LAB
echo ====================================================================
echo.

:: 1. Check for Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PY_CMD=python
    goto FOUND_PYTHON
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set PY_CMD=py
    goto FOUND_PYTHON
)

echo [ERROR] Python is not installed or not in your system PATH!
echo.
echo Please install Python:
echo 1. Download from: https://www.python.org/downloads/
echo 2. IMPORTANT: Check the box "Add Python to PATH" during installation!
echo.
pause
exit /b 1

:FOUND_PYTHON
echo [1/3] Detected Python: %PY_CMD%
%PY_CMD% --version

:: 2. Check and auto-install Selenium
echo.
echo [2/3] Checking dependencies (Selenium)...
%PY_CMD% -c "import selenium" >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing required testing package (Selenium)...
    %PY_CMD% -m pip install selenium
    if %errorlevel% neq 0 (
        echo [WARNING] Automatic pip install failed. You can still use the website,
        echo but automated tests will need: pip install selenium
    )
) else (
    echo [OK] Selenium is installed!
)

:: 3. Launch portal
echo.
echo [3/3] Starting web server and opening Google Chrome...
echo ====================================================================
echo Site will open in Chrome. Press Ctrl+C in this window to stop.
echo ====================================================================
echo.

%PY_CMD% run_portal.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The server stopped unexpectedly.
    pause
)
