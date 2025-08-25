@echo off
echo Starting Phishy AI Platform...
echo.

cd /d "%~dp0"

echo Checking Python environment...
python --version
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Starting backend server...
echo Backend will be available at: http://localhost:8080
echo API Documentation will be at: http://localhost:8080/docs
echo.
echo To view the frontend, open: frontend/index.html in your browser
echo Or serve it with: python -m http.server 3001 (in the frontend folder)
echo.

python app.py

pause