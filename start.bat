@echo off
chcp 65001
cls
echo ==========================================
echo     Text to Speech Tool - TTS
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [1/4] Checking Python environment... OK

REM Check .env file
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found
    echo Please copy .env.example to .env and fill in your AK/SK
    echo.
    copy .env.example .env
    echo .env file created. Please edit it and run again.
    notepad .env
    pause
    exit /b 1
)

echo [2/4] Checking environment variables... OK

REM Install dependencies
echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [3/4] Dependencies installed... OK

REM Start service
echo [4/4] Starting service...
echo.
echo ==========================================
echo Service is starting...
echo Browser will open automatically at http://localhost:8000
echo Press Ctrl+C to stop the service
echo ==========================================
echo.

REM Wait and open browser
timeout /t 3 /nobreak >nul
start http://localhost:8000

REM Start server
python main.py

pause
