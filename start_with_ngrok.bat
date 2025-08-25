@echo off
echo ====================================
echo    Starting Phishy with ngrok
echo ====================================

echo.
echo 1. Starting ngrok tunnel...
start /B ngrok http 8080

echo.
echo 2. Waiting for ngrok to start (10 seconds)...
timeout /t 10

echo.
echo 3. Getting ngrok URL and updating .env...
python get_ngrok_url.py

echo.
echo 4. Starting Phishy backend...
echo Press Ctrl+C to stop
echo.
python backend/app.py