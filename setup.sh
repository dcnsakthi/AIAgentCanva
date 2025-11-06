#!/bin/bash

# MAF Agent Builder - Setup Script
# This script helps you set up the application quickly

echo "🤖 MAF Agent Builder - Setup Script"
echo "==================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found: Python $PYTHON_VERSION"

# Check if version is 3.9 or higher
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 9 ]; then
    echo "❌ Python 3.9 or higher is required"
    exit 1
fi

echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"

echo ""

# Setup environment file
echo "Setting up environment configuration..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists"
else
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY or AZURE_OPENAI_* credentials"
    echo "   - Other optional services as needed"
fi

echo ""

# Create necessary directories
echo "Creating project directories..."
mkdir -p data logs user_projects templates deployed_agents
echo "✅ Project directories created"

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "For quick start guide, see: QUICKSTART.md"
echo "For full documentation, see: README.md"
echo ""

# Ask if user wants to open .env file
read -p "Do you want to open .env file now to configure API keys? (Y/n): " openEnv
if [ "$openEnv" != "n" ] && [ "$openEnv" != "N" ]; then
    ${EDITOR:-nano} .env
fi

echo ""
echo "Happy building! 🚀"
