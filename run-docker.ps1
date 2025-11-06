# AI Agent Canvas - Docker Setup
# Run all services: App, Backend API, ChromaDB, Redis, Ollama

Write-Host "🚀 Starting AI Agent Canvas with Docker..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if docker-compose exists
if (!(Test-Path "docker-compose.yml")) {
    Write-Host "✗ docker-compose.yml not found" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Found docker-compose.yml" -ForegroundColor Green
Write-Host ""

# Ask user for mode
Write-Host "Select mode:" -ForegroundColor Yellow
Write-Host "1. Demo Mode (no API keys required)"
Write-Host "2. Production Mode (requires API keys)"
$mode = Read-Host "Enter choice (1 or 2)"

if ($mode -eq "1") {
    Write-Host "📝 Running in Demo Mode" -ForegroundColor Cyan
    $env:APP_ENV = "demo"
    $env:OPENAI_API_KEY = "demo-mode"
} else {
    Write-Host "📝 Running in Production Mode" -ForegroundColor Cyan
    if (!(Test-Path ".env")) {
        Write-Host "⚠️  Warning: .env file not found. Copy .env.example to .env and configure it." -ForegroundColor Yellow
        Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "✓ Created .env file. Please edit it with your API keys." -ForegroundColor Green
        Write-Host "Then run this script again." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "🔨 Building Docker images..." -ForegroundColor Cyan
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Build complete" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start services" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Services started successfully!" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Show service status
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ AI Agent Canvas is ready!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access the application at:" -ForegroundColor Yellow
Write-Host "   Streamlit App:  http://localhost:8501" -ForegroundColor White
Write-Host "   Backend API:    http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "   ChromaDB:       http://localhost:8000" -ForegroundColor White
Write-Host "   Ollama:         http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "📝 View logs:" -ForegroundColor Yellow
Write-Host "   docker-compose logs -f app" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Stop services:" -ForegroundColor Yellow
Write-Host "   docker-compose down" -ForegroundColor White
Write-Host ""

# Try to open browser
Write-Host "🌐 Opening browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "Press Ctrl+C to exit (services will continue running)" -ForegroundColor Gray
