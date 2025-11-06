# 🚀 Quick Start - AI Agent Canvas

Choose your preferred method to run the application:

## Method 1: 🐳 Docker (Recommended for Production)

Best for: Complete setup with all services, production deployment

### Prerequisites
- Docker Desktop installed
- 8GB RAM allocated to Docker

### Steps

1. **Run the setup script:**
   ```powershell
   # Windows
   .\run-docker.ps1
   
   # Linux/Mac
   chmod +x run-docker.sh && ./run-docker.sh
   ```

2. **Access the application:**
   - Main App: http://localhost:8501
   - API Docs: http://localhost:8000/docs
   - ChromaDB: http://localhost:8000

### What You Get
✅ Streamlit web app
✅ Backend REST API
✅ ChromaDB vector database
✅ Redis caching
✅ Ollama local LLM (optional)
✅ All services connected automatically

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed documentation.

---

## Method 2: 💻 Local Python (Quick Testing)

Best for: Development, quick testing, minimal setup

### Prerequisites
- Python 3.11+ installed
- Virtual environment (recommended)

### Steps

1. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install demo dependencies:**
   ```powershell
   pip install -r requirements-demo.txt
   ```

3. **Run the application:**
   ```powershell
   streamlit run app.py
   ```

4. **Access at:** http://localhost:8501

### Demo Mode Features
✅ No API keys needed
✅ Simulated AI responses
✅ All UI features work
✅ Quick to start
⚠️ No actual LLM calls
⚠️ No vector database

---

## 🎯 Choosing the Right Method

| Feature | Docker | Local Python |
|---------|--------|--------------|
| Setup Time | 5-10 min | 2-3 min |
| Real LLM Support | ✅ Yes | ⚠️ Demo only |
| Vector Database | ✅ Yes | ❌ No |
| Backend API | ✅ Yes | ❌ No |
| Production Ready | ✅ Yes | ❌ No |
| Development | ✅ Yes | ✅ Yes |
| Resource Usage | High | Low |

**Use Docker if:**
- You want the full experience
- You need real LLM integration
- You're deploying to production
- You want all services (API, DB, etc.)

**Use Local Python if:**
- You just want to see the UI
- You're testing quickly
- You don't need real AI responses
- You have limited resources

---

## 🎮 First Steps After Launch

### 1. Login
Choose one of:
- **Demo Mode** (no signup needed) ← Start here!
- GitHub OAuth
- Microsoft Entra ID
- Email magic link

### 2. Create Your First Agent
1. Click "New Project"
2. Enter project details
3. Choose agent type (Assistant, Researcher, Coder, etc.)
4. Configure agent settings

### 3. Test Your Agent
1. Go to "Sandbox" tab
2. Chat with your agent
3. View metrics and responses

### 4. Deploy (Docker only)
1. Go to "Deployment" tab
2. Choose Azure target
3. Generate deployment scripts
4. Deploy to Azure

---

## 📚 Next Steps

- **Learn by Example:** See [EXAMPLES.md](EXAMPLES.md)
- **Full Documentation:** Read [README.md](README.md)
- **Docker Guide:** Check [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Project Summary:** Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🆘 Troubleshooting

### Local Python Issues

**Import errors:**
```powershell
pip install -r requirements.txt
```

**Port already in use:**
```powershell
streamlit run app.py --server.port=8502
```

### Docker Issues

**Services won't start:**
```bash
docker-compose logs -f
docker-compose down && docker-compose up -d
```

**Out of memory:**
- Docker Desktop → Settings → Resources → Memory (set to 8GB+)

**Build errors:**
```bash
docker-compose build --no-cache
```

---

## 💡 Tips

1. **Start with Demo Mode** to explore features
2. **Use Docker** for the complete experience
3. **Check logs** if something doesn't work
4. **Read examples** to learn best practices
5. **Join community** for help and updates

---

## 🚀 Ready to Go!

Choose your method above and start building AI agents in minutes!

**Questions?** Check the documentation or open an issue on GitHub.
