# MAF Agent Builder Canvas 🤖

> **Build powerful AI single or multi-agent systems using Microsoft Agent Framework (MAF) with an intuitive visual canvas interface**

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Overview

MAF Agent Builder Canvas is an enterprise-grade, visual development platform for creating sophisticated AI agent systems. Built on Microsoft Agent Framework (MAF) and Streamlit, it provides a drag-and-drop interface for composing single or multi-agent teams with support for:

- **Multiple LLM Providers**: Azure OpenAI, OpenAI, Anthropic
- **Vector Databases**: ChromaDB, FAISS, Pinecone, Qdrant, Weaviate
- **Visual Canvas Builder**: Drag-and-drop agent composition
- **Live Preview Sandbox**: Test agents in real-time
- **Evaluation Harness**: Automated testing and quality assurance
- **Azure Deployment**: One-click deployment to Azure Container Apps

## ✨ Key Features

### 📝 Prompt-to-Canvas Flow
- **Product Brief Landing Page**: Describe your agent system in natural language
- **Document-Grounded Prompts**: Attach documents, images, or select existing tools
- **Intelligent Generation**: AI-powered canvas initialization from your description

### 🎨 Visual Builder
- **Drag-and-Drop Interface**: Compose agents, team managers, and tools visually
- **Multiple Agent Types**:
  - 🤖 Assistant Agent - General-purpose conversational AI
  - 🔍 Research Agent - Information gathering and synthesis
  - 💻 Code Agent - Code generation and analysis
  - 📊 Data Analyst Agent - Data processing and visualization
  - 👔 Team Manager - Multi-agent coordination

### 🧪 Live Preview Sandbox
- **Real-time Testing**: Test agents without leaving the workspace
- **Conversation History**: Full chat history with metadata
- **Performance Metrics**: Token usage, response times, success rates

### 📚 Playbooks & Templates
- **Pre-built Templates**: Customer support, research, code review, data analysis
- **Reusable Scenes**: Save and share multi-agent configurations
- **Placeholder Slots**: Customize templates for your use case

### ✅ Evaluation Harness
- **Scripted Conversations**: Define expected behaviors with test cases
- **Assertions**: Multiple assertion types (contains, regex, length, etc.)
- **QA Suite Export**: Tests included with deployment bundles
- **Automated Testing**: Run full test suites with detailed reporting

### 🚀 Deployment & Authentication
- **Azure Container Apps**: Automated deployment with Bicep templates
- **Multiple Auth Methods**:
  - GitHub OAuth
  - Microsoft Entra (Azure AD)
  - Email Magic Links
  - Demo Mode
- **Infrastructure as Code**: Bicep, Azure CLI, PowerShell, Terraform support

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Azure subscription (for deployment)
- OpenAI API key or Azure OpenAI service

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd AIAgentCanva
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys and configuration
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Authentication

Choose your preferred authentication method:

- **Demo Mode**: Quick start without configuration
- **GitHub**: OAuth with your GitHub account
- **Microsoft**: Sign in with Microsoft Entra ID
- **Magic Link**: Passwordless email authentication

### 2. Create a Project

#### Option A: From Prompt
1. Click "New Project"
2. Enter project name and description
3. Attach optional documents for context
4. Select pre-built tools
5. Click "Generate & Open in Canvas"

#### Option B: From Template
1. Click "Templates"
2. Browse available templates
3. Select a template
4. Customize as needed

### 3. Build on Canvas

1. **Add Agents**: Click "➕ Add Agent" and select agent type
2. **Configure Properties**: Select an agent to edit its properties:
   - System prompt
   - LLM model and parameters
   - Tools and capabilities
   - Vector database connection
3. **Connect Agents**: Use "🔗 Connect" to link agents
4. **Save**: Click "💾 Save" to persist your changes

### 4. Test in Sandbox

1. Navigate to "🧪 Live Sandbox"
2. Select an agent to test
3. Type messages to interact with your agent
4. Review metrics and conversation history
5. Export conversations for analysis

### 5. Create Evaluations

1. Go to "✅ Evaluation"
2. Click "Create Test Case"
3. Define conversation turns
4. Add assertions to validate behavior
5. Run tests and review results

### 6. Deploy to Azure

1. Navigate to "🚀 Deployment"
2. Configure Azure settings:
   - Subscription and resource group
   - Azure region
   - Container Apps configuration
3. Generate deployment scripts (Bicep, CLI, PowerShell, or Terraform)
4. Review and download scripts
5. Deploy (dry-run first recommended)
6. Monitor your deployed agents

## 🏗️ Architecture

```
MAF Agent Builder Canvas
│
├── Authentication Layer
│   ├── GitHub OAuth
│   ├── Microsoft Entra ID
│   ├── Email Magic Links
│   └── Demo Mode
│
├── Visual Canvas Builder
│   ├── Drag-and-Drop Interface
│   ├── Agent Configuration
│   └── Connection Management
│
├── Agent Framework Core
│   ├── Agent Types & Factory
│   ├── LLM Provider Integration
│   ├── Vector Database Support
│   └── Tool Management
│
├── Live Sandbox
│   ├── Agent Execution
│   ├── Conversation Management
│   └── Metrics Collection
│
├── Evaluation System
│   ├── Test Case Management
│   ├── Assertion Engine
│   └── Results Reporting
│
└── Deployment Pipeline
    ├── Bicep Template Generation
    ├── Azure CLI Scripts
    ├── PowerShell Scripts
    └── Terraform Configuration
```

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example` for full list):

```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Vector Database
VECTOR_DB_TYPE=chromadb  # chromadb, faiss, pinecone, qdrant, weaviate

# Authentication
GITHUB_CLIENT_ID=your-github-client-id
MICROSOFT_CLIENT_ID=your-microsoft-client-id
JWT_SECRET_KEY=your-jwt-secret

# Azure Deployment
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=maf-agents-rg
```

### Application Configuration

Edit `config.yaml` to customize:

- Available LLM models
- Vector database options
- Agent types and defaults
- Canvas settings
- Evaluation metrics
- Deployment defaults

## 📚 Documentation

### Agent Types

#### Assistant Agent
General-purpose conversational agent for customer service, Q&A, and general tasks.

#### Research Agent
Specialized in information gathering, web search, and content synthesis.

#### Code Agent
Expert in code generation, analysis, debugging, and technical documentation.

#### Data Analyst Agent
Handles data processing, analysis, visualization, and reporting.

#### Team Manager Agent
Orchestrates multiple agents, delegates tasks, and synthesizes results.

### Vector Databases

Supported vector databases for knowledge retrieval:

- **ChromaDB**: Local, persistent vector store (default)
- **FAISS**: Facebook AI Similarity Search for efficient vector search
- **Pinecone**: Managed vector database service
- **Qdrant**: Vector similarity search engine
- **Weaviate**: Open-source vector search engine

### LLM Providers

Supported language models:

- **Azure OpenAI**: GPT-4, GPT-4-32K, GPT-3.5-Turbo
- **OpenAI**: GPT-4-Turbo, GPT-3.5-Turbo
- **Anthropic**: Claude 3 (coming soon)

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest --cov=src tests/
```

## 🚀 Deployment

### Deploy to Azure Container Apps

1. **Using Azure CLI**:
```bash
# Generate scripts
# Download from Deployment page

# Run deployment
./deploy.sh
```

2. **Using PowerShell**:
```powershell
.\deploy.ps1
```

3. **Using Terraform**:
```bash
terraform init
terraform plan
terraform apply
```

### Docker Deployment

```bash
# Build image
docker build -t maf-agent-builder .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  maf-agent-builder
```

## 📊 Project Structure

```
AIAgentCanva/
├── app.py                          # Main Streamlit application
├── config.yaml                     # Application configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── src/
│   ├── agents/                     # Agent framework
│   │   ├── agent_types.py         # Agent type definitions
│   │   ├── agent_executor.py      # Agent execution engine
│   │   ├── project_generator.py   # Project generator from prompts
│   │   └── implementations/       # Agent implementations
│   ├── auth/                       # Authentication
│   │   └── auth_manager.py        # Multi-provider auth
│   ├── ui/                         # User interface
│   │   └── pages/                 # Streamlit pages
│   │       ├── landing.py         # Landing page
│   │       ├── canvas.py          # Canvas builder
│   │       ├── sandbox.py         # Live sandbox
│   │       ├── evaluation.py      # Evaluation harness
│   │       └── deployment.py      # Deployment interface
│   ├── evaluation/                 # Testing framework
│   │   ├── test_runner.py         # Test execution
│   │   └── test_case.py           # Test case definitions
│   ├── deployment/                 # Deployment automation
│   │   ├── azure_deployer.py      # Azure deployment
│   │   └── bicep_generator.py     # IaC generation
│   └── utils/                      # Utilities
│       └── config_loader.py       # Configuration loader
├── templates/                      # Agent templates
├── tests/                          # Test suite
└── docs/                           # Additional documentation
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Microsoft Agent Framework (MAF)** for the agent orchestration framework
- **Streamlit** for the amazing web app framework
- **Azure** for cloud infrastructure and AI services
- **OpenAI** for language models

## 📧 Support

- 📖 [Documentation](docs/)
- 💬 [Discussions](https://github.com/your-repo/discussions)
- 🐛 [Issue Tracker](https://github.com/your-repo/issues)
- 📧 Email: support@example.com

## 🗺️ Roadmap

- [ ] Additional LLM providers (Anthropic Claude, Google PaLM)
- [ ] Enhanced vector database integration
- [ ] Real-time collaboration features
- [ ] Advanced monitoring and observability
- [ ] Multi-language support
- [ ] Mobile-responsive interface
- [ ] Plugin system for custom tools
- [ ] Marketplace for agent templates

---

**Built with ❤️ using Microsoft Agent Framework and Streamlit**
