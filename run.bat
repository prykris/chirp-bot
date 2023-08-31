@echo off
setlocal

:: Detect the operating system
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
set "OS=Unknown"

if "%VERSION%" == "10.0" (
    set "OS=Windows 10"
) else (
    echo OS not recognized: %VERSION%
    exit /b 1
)

:: Activate virtual environment
if "%OS%" == "Windows 10" (
    call venv\Scripts\activate
) else (
    echo OS not recognized: %OS%
    exit /b 1
)

:: Check if selenium is installed
python -c "import selenium" 2>nul
if errorlevel 1 (
    pip install -r requirements.txt
)

:: Navigate to src directory and run main Python script
cd src || (
    echo "Failed to change directory to src."
    exit /b 1
)

echo Running main.py
python main.py

endlocal