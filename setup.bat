@echo off
echo SecurityNexus Installation Assistant
echo ==============================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.6 or higher.
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

echo Python installation found. Installing dependencies...
echo.

pip install -r config/requirements.txt

if %errorlevel% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b
)

echo Dependencies installed successfully.
echo.
echo SecurityNexus is ready to use! You can start it by running the start.bat file.
echo.
pause 