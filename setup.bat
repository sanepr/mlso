@echo off
REM MLOps Heart Disease Prediction - Windows Startup Script
REM This script automates the setup and initialization of the project

setlocal enabledelayedexpansion

echo ========================================
echo   MLOps Heart Disease Prediction
echo   Automated Setup Script (Windows)
echo ========================================
echo.

REM Check if Python is installed
echo [i] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is not installed. Please install Python 3.9+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✓] Python %PYTHON_VERSION% detected
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] pip is not installed. Please install pip first.
    pause
    exit /b 1
)
echo [✓] pip detected
echo.

REM Create virtual environment
echo [i] Creating virtual environment...
if exist venv (
    echo [i] Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo [✓] Virtual environment created
)
echo.

REM Activate virtual environment
echo [i] Activating virtual environment...
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated
echo.

REM Upgrade pip
echo [i] Upgrading pip...
python -m pip install --upgrade pip -q
echo [✓] pip upgraded
echo.

REM Install requirements
echo [i] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [X] Failed to install dependencies. Please check requirements.txt
    pause
    exit /b 1
)
echo [✓] Dependencies installed
echo.

REM Create necessary directories
echo [i] Creating project directories...
if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed
if not exist models mkdir models
if not exist logs mkdir logs
if not exist screenshots mkdir screenshots
if not exist mlruns mkdir mlruns
echo [✓] Directories created
echo.

REM Download dataset
echo [i] Downloading Heart Disease dataset...
if exist data\raw\heart.csv (
    echo [i] Dataset already exists. Skipping download.
) else (
    python src\data\download_data.py
    if %errorlevel% neq 0 (
        echo [X] Failed to download dataset.
        pause
        exit /b 1
    )
    echo [✓] Dataset downloaded
)
echo.

REM Preprocess data
echo [i] Preprocessing data...
if exist data\processed\X_train.pkl (
    echo [i] Preprocessed data already exists. Skipping preprocessing.
) else (
    python src\data\preprocessing.py
    if %errorlevel% neq 0 (
        echo [X] Failed to preprocess data.
        pause
        exit /b 1
    )
    echo [✓] Data preprocessed
)
echo.

REM Run tests
echo [i] Running tests...
pytest tests\ -v --tb=short
if %errorlevel% equ 0 (
    echo [✓] All tests passed
) else (
    echo [!] Some tests failed. Please check the output above.
)
echo.

REM Train models (optional)
set /p TRAIN_MODELS="Do you want to train the models now? (y/n): "
if /i "%TRAIN_MODELS%"=="y" (
    echo [i] Training models with MLflow tracking...
    python src\models\train.py
    if %errorlevel% equ 0 (
        echo [✓] Models trained successfully
    ) else (
        echo [X] Model training failed.
    )
) else (
    echo [i] Skipping model training. You can train later with: python src\models\train.py
)
echo.

REM Setup complete
echo ========================================
echo   Setup Complete! 🎉
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Activate virtual environment (if not already active):
echo    venv\Scripts\activate
echo.
echo 2. Start Jupyter for EDA:
echo    jupyter notebook notebooks\01_eda.ipynb
echo.
echo 3. Train models (if skipped):
echo    python src\models\train.py
echo.
echo 4. View MLflow UI:
echo    mlflow ui
echo.
echo 5. Start the API server:
echo    python src\api\app.py
echo.
echo 6. Run tests:
echo    pytest tests\ -v
echo.
echo 7. Build Docker image:
echo    docker build -t heart-disease-api:latest .
echo.
echo Documentation:
echo   - README.md for project overview
echo   - QUICK_START.md for detailed instructions
echo.
echo Happy MLOps! 🚀
echo.
pause
