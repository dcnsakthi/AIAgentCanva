# 🐳 Docker Setup Guide

This guide explains how to run AI Agent Canvas using Docker with all required backend services.

## 📋 Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** (usually included with Docker Desktop)
- At least **8GB RAM** allocated to Docker
- **10GB free disk space**

## 🏗️ Architecture

The Docker setup includes the following services:

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent Canvas                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Streamlit   │  │  Backend API │  │   ChromaDB   │      │
│  │    App       │◄─┤   FastAPI    │◄─┤  Vector DB   │      │
│  │  :8501       │  │   :8000      │  │   :8000      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                   │              │
│         │                 └───────┬───────────┘              │
│         │                         │                          │
│  ┌──────┴──────┐  ┌──────────────┴┐  ┌──────────────┐      │
│  │   Redis     │  │    Ollama     │  │   Qdrant     │      │
│  │   Cache     │  │  Local LLM    │  │  Vector DB   │      │
│  │   :6379     │  │   :11434      │  │   :6333      │      │
│  └─────────────┘  └───────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Services

1. **Streamlit App** (`:8501`) - Main web interface
2. **Backend API** (`:8000`) - FastAPI service for agent execution
3. **ChromaDB** (`:8000`) - Default vector database
4. **Redis** (`:6379`) - Caching and message queue
5. **Ollama** (`:11434`) - Local LLM models (optional)
6. **Qdrant** (`:6333`) - Alternative vector database (optional)
7. **PostgreSQL** (`:5432`) - Production database (optional)

## 🚀 Quick Start

### Option 1: Using the Setup Script (Recommended)

**Windows (PowerShell):**
```powershell
.\run-docker.ps1
```

**Linux/Mac:**
```bash
chmod +x run-docker.sh
./run-docker.sh
```

The script will:
- Check Docker installation
- Build all images
- Start all services
- Open the app in your browser

### Option 2: Manual Docker Compose

**Demo Mode (No API keys required):**
```bash
# Set environment
export APP_ENV=demo
export OPENAI_API_KEY=demo-mode

# Build and start
docker-compose build
docker-compose up -d
```

**Production Mode:**
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Build and start
docker-compose build
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables

Edit `.env` file for production configuration:

```env
# Mode
APP_ENV=production  # or 'demo'

# OpenAI (Optional)
OPENAI_API_KEY=sk-...

# Azure OpenAI (Optional)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Authentication (Optional)
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
MICROSOFT_CLIENT_ID=...
MICROSOFT_CLIENT_SECRET=...
```

### Resource Allocation

Edit `docker-compose.yml` to adjust resources:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## 📦 Service Details

### ChromaDB (Vector Database)

**Purpose:** Store and retrieve embeddings for RAG
**Access:** http://localhost:8000
**Data:** Persisted in `chromadb-data` volume

### Ollama (Local LLM)

**Purpose:** Run LLMs locally without API costs
**Access:** http://localhost:11434
**Data:** Persisted in `ollama-data` volume

**Pull models:**
```bash
docker-compose exec ollama ollama pull llama2
docker-compose exec ollama ollama pull codellama
docker-compose exec ollama ollama pull mistral
```

**List models:**
```bash
docker-compose exec ollama ollama list
```

### Backend API

**Purpose:** REST API for agent operations
**Access:** http://localhost:8000
**Docs:** http://localhost:8000/docs (Swagger UI)

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/agent/execute` - Execute agent
- `POST /api/v1/agent/execute/stream` - Stream execution
- `GET /api/v1/models/available` - List models
- `GET /api/v1/vectordb/collections` - List collections

## 🛠️ Common Operations

### View Logs

**All services:**
```bash
docker-compose logs -f
```

**Specific service:**
```bash
docker-compose logs -f app
docker-compose logs -f backend
docker-compose logs -f chromadb
```

### Stop Services

**Stop but keep data:**
```bash
docker-compose stop
```

**Stop and remove containers:**
```bash
docker-compose down
```

**Stop and remove all data:**
```bash
docker-compose down -v
```

### Restart Service

```bash
docker-compose restart app
docker-compose restart backend
```

### Rebuild After Changes

```bash
docker-compose build app
docker-compose up -d app
```

### Check Service Status

```bash
docker-compose ps
```

### Execute Commands in Container

```bash
docker-compose exec app bash
docker-compose exec backend python -c "import sys; print(sys.version)"
```

## 🔍 Troubleshooting

### Service Won't Start

**Check logs:**
```bash
docker-compose logs app
```

**Check if port is in use:**
```bash
# Windows
netstat -ano | findstr :8501

# Linux/Mac
lsof -i :8501
```

### Out of Memory

**Increase Docker memory:**
- Docker Desktop → Settings → Resources → Memory
- Set to at least 8GB

### ChromaDB Connection Error

**Check if ChromaDB is running:**
```bash
curl http://localhost:8000/api/v1/heartbeat
```

**Restart ChromaDB:**
```bash
docker-compose restart chromadb
```

### Ollama GPU Support

**NVIDIA GPU (Linux):**
```bash
# Install nvidia-docker2
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

**For CPU-only, remove GPU section from docker-compose.yml:**
```yaml
# Remove this section
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

### Build Failures

**Clear Docker cache:**
```bash
docker-compose build --no-cache
docker system prune -a
```

## 📊 Monitoring

### Resource Usage

```bash
docker stats
```

### Disk Usage

```bash
docker system df
```

### Container Health

```bash
docker-compose ps
docker inspect <container-name> | grep Health
```

## 🔐 Security

### Production Checklist

- [ ] Change all default passwords in `.env`
- [ ] Set strong `JWT_SECRET_KEY`
- [ ] Configure `CORS_ORIGINS` to specific domains
- [ ] Use HTTPS reverse proxy (nginx, Caddy)
- [ ] Enable firewall rules
- [ ] Use Docker secrets for sensitive data
- [ ] Regularly update images: `docker-compose pull`
- [ ] Backup volumes: `docker run --rm -v chromadb-data:/data -v $(pwd):/backup alpine tar czf /backup/chromadb-backup.tar.gz /data`

## 🚀 Deployment

### Deploy to Azure Container Instances

```bash
# Install Azure CLI
az login

# Create resource group
az group create --name ai-agent-rg --location eastus

# Deploy with docker-compose
az container create \
  --resource-group ai-agent-rg \
  --file docker-compose.yml \
  --dns-name-label ai-agent-canvas
```

### Deploy to AWS ECS

Use the deployment scripts:
```bash
python src/deployment/deploy_to_aws.py
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Ollama Models](https://ollama.ai/library)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 💡 Tips

1. **Use Demo Mode** for testing without API keys
2. **Pull Ollama models** beforehand to avoid waiting
3. **Monitor memory** usage with `docker stats`
4. **Backup volumes** regularly in production
5. **Use .dockerignore** to exclude unnecessary files from builds

## 🆘 Getting Help

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify services: `docker-compose ps`
3. Check health: `curl http://localhost:8501/_stcore/health`
4. Review this guide's troubleshooting section
5. Open an issue on GitHub with logs and error messages
