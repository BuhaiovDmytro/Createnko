@echo off
title Facebook Ads Video Generator
color 0A

echo.
echo  ███████╗ █████╗  ██████╗███████╗███████╗███████╗    ██████╗  █████╗ ██████╗ ██╗   ██╗
echo  ██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝    ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██║     █████╗  █████╗  █████╗      ██████╔╝███████║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║     ██╔══╝  ██╔══╝  ██╔══╝      ██╔══██╗██╔══██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║╚██████╗███████╗███████╗███████╗    ██║  ██║██║  ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo                    Facebook Ads Library Video Generator
echo.
echo ========================================
echo   Starting Services...
echo ========================================
echo.

echo [1/4] Stopping existing services...
taskkill /f /im python.exe
taskkill /f /im node.exe
taskkill /f /im npm.cmd
timeout /t 2 /nobreak

echo [2/4] Setting up environment...
if not exist .env (
    copy env_template.txt .env
    echo [SUCCESS] .env file created
) else (
    echo [INFO] .env file already exists
)

echo [3/4] Starting API Server...
REM Try different Python paths
if exist "C:\Program Files\Python312\python.exe" (
    start /min "API Server" cmd /c "C:\Program Files\Python312\python.exe api_server.py"
) else if exist "C:\Program Files\Python311\python.exe" (
    start /min "API Server" cmd /c "C:\Program Files\Python311\python.exe api_server.py"
) else if exist "C:\Program Files\Python310\python.exe" (
    start /min "API Server" cmd /c "C:\Program Files\Python310\python.exe api_server.py"
) else (
    start /min "API Server" cmd /c "python api_server.py"
)
timeout /t 5 /nobreak

echo [4/4] Starting Frontend...
cd frontend
REM Add Node.js to PATH
set PATH=%PATH%;%~dp0nodejs\node-v20.11.0-win-x64
REM Check if npm is available
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found in PATH. Trying direct path...
    start /min "Frontend Server" cmd /c "%~dp0nodejs\node-v20.11.0-win-x64\npm.cmd start"
) else (
    start /min "Frontend Server" cmd /c "npm start"
)
cd ..

echo.
echo ========================================
echo   Checking Services Status...
echo ========================================
echo.

REM Wait a bit for services to start
timeout /t 3 /nobreak >nul

REM Check API Server
netstat -an | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ✅ API Server: Running on port 8000
) else (
    echo ❌ API Server: Not running on port 8000
)

REM Check Frontend
netstat -an | findstr :3000 >nul
if %errorlevel% equ 0 (
    echo ✅ Frontend: Running on port 3000
) else (
    echo ❌ Frontend: Not running on port 3000
)

echo.
echo ========================================
echo   Services Started Successfully!
echo ========================================
echo.
echo 🌐 Frontend:  http://localhost:3000
echo 🔧 API:       http://localhost:8000
echo 📚 API Docs:  http://localhost:8000/docs
echo.
echo [INFO] Services are running in background windows
echo [INFO] Use restart.bat to restart services
echo.
pause