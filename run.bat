@echo off
setlocal

:: Check if the shell is PowerShell
powershell -command "if ($Host.Name -eq 'ConsoleHost') { exit 0 } else { exit 1 }"
if %errorlevel%==0 (
    echo Running in PowerShell
    powershell -command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
) else (
    echo Running in Command Prompt
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python.
    pause
    exit /b 1
)

:: Check if virtual environment exists and activate it
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate
) else (
    echo Virtual environment does not exist.
    choice /M "Do you want to set up a virtual environment? (Y/N)"
    if errorlevel 2 (
        echo Exiting without virtual environment.
        pause
        exit /b 1
    ) else (
        python -m venv venv
        call venv\Scripts\activate
    )
)

:: Check if selenium is installed
python -c "import selenium" 2>nul
if errorlevel 1 (
    echo Selenium is not installed. Installing requirements...
    pip install -r requirements.txt
)

:: Navigate to src directory and run main Python script
cd src || (
    echo "Failed to change directory to src."
    pause
    exit /b 1
)

echo Running main.py
python main.py

pause
endlocal