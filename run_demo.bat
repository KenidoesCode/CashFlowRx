@echo off
echo ================================
echo Bank Risk Analyzer Demo Launcher
echo ================================

REM Check Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Please install Python 3.10+
    pause
    exit /b
)



REM Install deps (safe if already installed)
pip install -r requirements.txt

REM Run app
streamlit run app.py


pause
