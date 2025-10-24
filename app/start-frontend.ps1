# ============================================
# Start Frontend Locally (Without Docker)
# ============================================

Write-Host "`n🚀 Starting Frontend Server...`n" -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location "d:\12123\Diabetes-Detection-System\monorepo-example\frontend"

# Install dependencies if not already installed
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Start Vite dev server
Write-Host "`n✅ Frontend starting on http://localhost:5173`n" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔌 Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

npm run dev
