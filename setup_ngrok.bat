@echo off
echo ====================================
echo     Phishy ngrok Setup Helper
echo ====================================
echo.
echo STEP 1: Download ngrok
echo Visit: https://ngrok.com/download
echo Download the Windows version and extract to C:\ngrok\
echo.
echo STEP 2: Get Auth Token  
echo Visit: https://dashboard.ngrok.com/get-started/your-authtoken
echo Copy your auth token
echo.
echo STEP 3: Setup ngrok
echo Run these commands in Command Prompt:
echo   cd C:\ngrok
echo   ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
echo.
echo STEP 4: Start ngrok tunnel
echo   ngrok http 8080
echo.
echo STEP 5: Update .env file
echo Copy the ngrok URL (like https://abc123-def456.ngrok-free.app)
echo Edit .env file and change:
echo   BASE_URL=https://your-ngrok-url-here.ngrok-free.app
echo.
echo STEP 6: Restart Phishy
echo Restart your backend server to use the new URL
echo.
echo ====================================
echo Then generate and send a new email!
echo The tracking pixel will use the public ngrok URL
echo ====================================
pause