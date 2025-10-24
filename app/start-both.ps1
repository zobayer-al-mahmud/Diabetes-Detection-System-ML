# ============================================
# Start Both Backend and Frontend Locally
# ============================================

Write-Host "`n🚀 Starting Full-Stack App Locally (No Docker)...`n" -ForegroundColor Cyan

# Start Backend in background
Write-Host "📦 Starting Backend..." -ForegroundColor Yellow
Start-Job -Name "Backend" -ScriptBlock {
    Set-Location "d:\12123\Diabetes-Detection-System\monorepo-example\backend"
    
    if (-not (Test-Path "venv")) {
        python -m venv venv
    }
    
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt -q
    $env:FRONTEND_URL = "http://localhost:5173"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
} | Out-Null

Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Gray
Start-Sleep -Seconds 8

# Start Frontend in background
Write-Host "🎨 Starting Frontend..." -ForegroundColor Yellow
Start-Job -Name "Frontend" -ScriptBlock {
    Set-Location "d:\12123\Diabetes-Detection-System\monorepo-example\frontend"
    
    if (-not (Test-Path "node_modules")) {
        npm install
    }
    
    npm run dev
} | Out-Null

Write-Host "⏳ Waiting for frontend to start..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "`n✅ Both services are starting!`n" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔌 Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

Write-Host "`n📋 Showing Backend Logs (Press Ctrl+C to stop all services)...`n" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Show logs and wait
try {
    while ($true) {
        $backendOutput = Receive-Job -Name "Backend" -ErrorAction SilentlyContinue
        if ($backendOutput) {
            Write-Host $backendOutput -ForegroundColor White
        }
        
        $frontendOutput = Receive-Job -Name "Frontend" -ErrorAction SilentlyContinue
        if ($frontendOutput) {
            Write-Host $frontendOutput -ForegroundColor Gray
        }
        
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Write-Host "`n🛑 Stopping all services..." -ForegroundColor Red
    Get-Job | Stop-Job
    Get-Job | Remove-Job
    Write-Host "✅ All services stopped.`n" -ForegroundColor Green
}
