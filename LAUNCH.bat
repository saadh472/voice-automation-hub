@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

title Voice Automation Hub
color 0B
cls

echo.
echo ========================================
echo   VOICE AUTOMATION HUB
echo ========================================
echo.

REM Check Java
echo Checking Java...
java -version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Java not found! Please install Java 11+
    pause
    exit /b 1
)
echo [OK] Java found

REM Check Node.js
echo Checking Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js
    pause
    exit /b 1
)
echo [OK] Node.js found

echo.
echo Starting servers...
echo.

REM Start Backend
echo [1/2] Starting Backend (port 8080)...
(
    echo @echo off
    echo cd /d "%~dp0backend"
    echo call mvnw.cmd spring-boot:run
) > "%TEMP%\start_backend.bat"
start "Backend" /min cmd /k "%TEMP%\start_backend.bat"
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [2/2] Starting Frontend (port 3000)...
if not exist "frontend\node_modules" (
    echo Installing dependencies...
    cd /d "%~dp0frontend"
    call npm install >nul 2>&1
    cd /d "%~dp0"
)
(
    echo @echo off
    echo cd /d "%~dp0frontend"
    echo call npm run dev
) > "%TEMP%\start_frontend.bat"
start "Frontend" /min cmd /k "%TEMP%\start_frontend.bat"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   Application Starting...
echo ========================================
echo.
echo   Backend:  http://localhost:8080
echo   Frontend: http://localhost:3000
echo.
echo   Please wait 30-60 seconds for servers to start
echo   Then the browser will open automatically
echo.

REM Wait and open browser
timeout /t 30 /nobreak >nul
start http://localhost:3000

echo Browser opened!
echo.
echo Keep the Backend and Frontend windows open.
echo Press any key to close this window...
pause >nul

endlocal
