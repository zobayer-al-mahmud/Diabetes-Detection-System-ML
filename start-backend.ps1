# ============================================
# Start Backend Locally (Without Docker)
# ============================================

Write-Host "`n🚀 Starting Backend Server...`n" -ForegroundColor Cyan

# Navigate to backend directory
Set-Location "d:\12123\Diabetes-Detection-System\monorepo-example\backend"

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# Set environment variable
$env:FRONTEND_URL = "http://localhost:5173"

# Start server
Write-Host "`n✅ Backend starting on http://localhost:8000`n" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🌐 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

uvicorn main:app --reload --host 0.0.0.0 --port 8000
