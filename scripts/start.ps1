# Facebook Ads Library Video Generator - Start Services
# Simple PowerShell script that works reliably

$Host.UI.RawUI.WindowTitle = "Facebook Ads Video Generator"

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ███████╗ █████╗  ██████╗███████╗███████╗███████╗    ██████╗  █████╗ ██████╗ ██╗   ██╗" -ForegroundColor Cyan
    Write-Host "  ██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝    ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝" -ForegroundColor Cyan
    Write-Host "  ███████╗███████║██║     █████╗  █████╗  █████╗      ██████╔╝███████║██████╔╝ ╚████╔╝ " -ForegroundColor Cyan
    Write-Host "  ╚════██║██╔══██║██║     ██╔══╝  ██╔══╝  ██╔══╝      ██╔══██╗██╔══██║██╔══██╗  ╚██╔╝  " -ForegroundColor Cyan
    Write-Host "  ███████║██║  ██║╚██████╗███████╗███████╗███████╗    ██║  ██║██║  ██║██║  ██║   ██║   " -ForegroundColor Cyan
    Write-Host "  ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   " -ForegroundColor Cyan
    Write-Host ""
    Write-Host "                    Facebook Ads Library Video Generator" -ForegroundColor Cyan
    Write-Host ""
}

function Stop-AllServices {
    Write-Host "[1/4] Stopping existing services..." -ForegroundColor Yellow
    
    # Stop Python processes
    Get-Process | Where-Object { $_.ProcessName -like "*python*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    # Stop Node.js processes
    Get-Process | Where-Object { $_.ProcessName -like "*node*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    # Stop npm processes
    Get-Process | Where-Object { $_.ProcessName -like "*npm*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Start-Sleep -Seconds 2
    Write-Host "[SUCCESS] Existing services stopped" -ForegroundColor Green
}

function Setup-Environment {
    Write-Host "[2/4] Setting up environment..." -ForegroundColor Yellow
    
    # Create .env file if needed
    if (-not (Test-Path ".env")) {
        Copy-Item "env_template.txt" ".env" -ErrorAction SilentlyContinue
        Write-Host "[SUCCESS] .env file created" -ForegroundColor Green
    } else {
        Write-Host "[INFO] .env file already exists" -ForegroundColor Green
    }
}

function Start-APIServer {
    Write-Host "[3/4] Starting API Server..." -ForegroundColor Yellow
    
    # Start API server
    Start-Process -FilePath "C:\Program Files\Python312\python.exe" -ArgumentList "api_server.py" -WindowStyle Minimized
    
    # Wait for API to start
    Write-Host "[INFO] Waiting for API to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Check API health
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "[SUCCESS] API Server is running!" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] API Server not responding properly" -ForegroundColor Red
        }
    } catch {
        Write-Host "[WARNING] API Server may still be starting..." -ForegroundColor Yellow
    }
}

function Start-Frontend {
    Write-Host "[4/4] Starting Frontend..." -ForegroundColor Yellow
    
    # Change to frontend directory
    Set-Location "frontend"
    
    # Add Node.js to PATH
    $env:PATH += ";C:\Users\$env:USERNAME\Desktop\GuruTrend\facebook-ads-library-mcp\nodejs\node-v20.11.0-win-x64"
    
    # Start frontend
    Start-Process -FilePath "cmd" -ArgumentList "/c", "npm start" -WindowStyle Minimized
    
    # Return to root directory
    Set-Location ".."
    
    Write-Host "[SUCCESS] Frontend started!" -ForegroundColor Green
}

function Show-Success {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Services Started Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Frontend:  http://localhost:3000" -ForegroundColor Cyan
    Write-Host "🔧 API:       http://localhost:8000" -ForegroundColor Cyan
    Write-Host "📚 API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[INFO] Services are running in background windows" -ForegroundColor Yellow
    Write-Host "[INFO] Use restart.ps1 to restart services" -ForegroundColor Yellow
    Write-Host ""
}

# Main execution
Show-Banner

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Services..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Stop-AllServices
Setup-Environment
Start-APIServer
Start-Frontend
Show-Success

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

