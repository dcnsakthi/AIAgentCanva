#!/bin/bash
# AI Agent Canvas - Docker Setup
# Run all services: App, Backend API, ChromaDB, Redis, Ollama

echo "🚀 Starting AI Agent Canvas with Docker..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "✗ Docker is not running. Please start Docker."
    exit 1
fi
echo "✓ Docker is running"

# Check if docker-compose exists
if [ ! -f "docker-compose.yml" ]; then
    echo "✗ docker-compose.yml not found"
    exit 1
fi
echo "✓ Found docker-compose.yml"
echo ""

# Ask user for mode
echo "Select mode:"
echo "1. Demo Mode (no API keys required)"
echo "2. Production Mode (requires API keys)"
read -p "Enter choice (1 or 2): " mode

if [ "$mode" == "1" ]; then
    echo "📝 Running in Demo Mode"
    export APP_ENV=demo
    export OPENAI_API_KEY=demo-mode
else
    echo "📝 Running in Production Mode"
    if [ ! -f ".env" ]; then
        echo "⚠️  Warning: .env file not found. Copy .env.example to .env and configure it."
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "✓ Created .env file. Please edit it with your API keys."
        echo "Then run this script again."
        exit 0
    fi
fi

echo ""
echo "🔨 Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "✗ Build failed"
    exit 1
fi
echo "✓ Build complete"
echo ""

echo "🚀 Starting services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "✗ Failed to start services"
    exit 1
fi
echo ""
echo "✓ Services started successfully!"
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Show service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ AI Agent Canvas is ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access the application at:"
echo "   Streamlit App:  http://localhost:8501"
echo "   Backend API:    http://localhost:8000"
echo "   API Docs:       http://localhost:8000/docs"
echo "   ChromaDB:       http://localhost:8000"
echo "   Ollama:         http://localhost:11434"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f app"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""

# Try to open browser (Linux)
if command -v xdg-open > /dev/null; then
    echo "🌐 Opening browser..."
    sleep 3
    xdg-open http://localhost:8501 2>/dev/null &
fi

echo "Press Ctrl+C to exit (services will continue running)"
