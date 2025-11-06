# MAF Agent Builder - Setup Script
# This script helps you set up the application quickly

Write-Host "🤖 MAF Agent Builder - Setup Script" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
            Write-Host "❌ Python 3.9 or higher is required" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9 or higher" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "✅ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green

Write-Host ""

# Setup environment file
Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
} else {
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env file and add your API keys:" -ForegroundColor Yellow
    Write-Host "   - OPENAI_API_KEY or AZURE_OPENAI_* credentials" -ForegroundColor White
    Write-Host "   - Other optional services as needed" -ForegroundColor White
}

Write-Host ""

# Create necessary directories
Write-Host "Creating project directories..." -ForegroundColor Yellow
$dirs = @("data", "logs", "user_projects", "templates", "deployed_agents")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}
Write-Host "✅ Project directories created" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and add your API keys" -ForegroundColor White
Write-Host "2. Run the application:" -ForegroundColor White
Write-Host "   streamlit run app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "For quick start guide, see: QUICKSTART.md" -ForegroundColor White
Write-Host "For full documentation, see: README.md" -ForegroundColor White
Write-Host ""

# Ask if user wants to open .env file
$openEnv = Read-Host "Do you want to open .env file now to configure API keys? (Y/n)"
if ($openEnv -ne 'n' -and $openEnv -ne 'N') {
    notepad .env
}

Write-Host ""
Write-Host "Happy building! 🚀" -ForegroundColor Cyan
