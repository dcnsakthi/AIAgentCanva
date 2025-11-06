# MAF Agent Builder - Quick Start Guide

## 🎯 Getting Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 minute)

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Run the Application (30 seconds)

```bash
streamlit run app.py
```

### Step 4: Create Your First Agent (1.5 minutes)

1. **Login**: Use Demo Mode (no setup required)
2. **Create Project**: Click "New Project"
   - Name: "Customer Support Bot"
   - Description: "An AI agent to help customers with product questions"
   - Click "Generate & Open in Canvas"
3. **Test Your Agent**: Go to "Live Sandbox" and start chatting!

## 🎓 Tutorials

### Tutorial 1: Build a Simple Assistant

```python
# This is automatically generated when you create a project
# Your agent will be configured with:
# - Type: Assistant Agent
# - Model: GPT-4
# - System Prompt: Custom based on your description
```

### Tutorial 2: Create a Multi-Agent Team

1. Create a new project
2. Select "Multi-Agent Team"
3. Add these agents on canvas:
   - Team Manager (coordinates)
   - Research Agent (gathers info)
   - Support Agent (responds)
4. Connect them: Manager → Research → Support
5. Test the workflow in sandbox

### Tutorial 3: Add Evaluation Tests

1. Go to Evaluation tab
2. Create a test case:
   - Name: "Greeting Test"
   - Conversation: "Hello" → Agent should greet warmly
   - Assertion: Response contains "welcome" or "help"
3. Run the test
4. Export results

### Tutorial 4: Deploy to Azure

1. Configure Azure settings in Deployment tab
2. Generate Bicep templates
3. Review the generated scripts
4. Run deployment (dry-run first)
5. Access your live agent URL

## 🛠️ Common Use Cases

### Use Case 1: Customer Support System
- **Template**: Customer Support Team
- **Agents**: Triage → Support → Escalation
- **Tools**: Knowledge base, ticketing system
- **Deployment**: Azure Container Apps with auto-scaling

### Use Case 2: Research Assistant
- **Template**: Research Assistant
- **Agents**: Single research agent
- **Tools**: Web search, document processing
- **Vector DB**: ChromaDB for document retrieval

### Use Case 3: Code Review Pipeline
- **Template**: Code Review Pipeline
- **Agents**: Analyzer → Tester → Reviewer → Reporter
- **Tools**: Code execution, static analysis
- **Deployment**: GitHub Actions integration

### Use Case 4: Data Analysis Workflow
- **Template**: Data Analysis Workflow
- **Agents**: Extractor → Analyzer → Visualizer → Reporter
- **Tools**: Data processing, charting
- **Vector DB**: FAISS for large datasets

## 🔧 Configuration Tips

### Optimizing Performance

```yaml
# config.yaml
agent_types:
  - temperature: 0.5  # More deterministic
  - max_tokens: 1500  # Balance quality/cost
```

### Choosing the Right Model

- **GPT-4**: Best quality, higher cost
- **GPT-3.5-Turbo**: Fast, cost-effective
- **GPT-4-32K**: Large context windows

### Vector Database Selection

- **ChromaDB**: Best for local development
- **FAISS**: Best for performance
- **Pinecone**: Best for production scale
- **Qdrant**: Best for hybrid search

## 📊 Monitoring Your Agents

### Key Metrics to Track

1. **Response Time**: Aim for < 2 seconds
2. **Token Usage**: Monitor costs
3. **Success Rate**: Target > 95%
4. **User Satisfaction**: Collect feedback

### Debugging Tips

```python
# Enable debug mode in sandbox
debug_mode = True  # Shows detailed logs

# Check agent logs
st.session_state.sandbox_messages  # View conversation history
```

## 🚨 Troubleshooting

### Problem: "API Key not found"
**Solution**: Check `.env` file has `OPENAI_API_KEY` set

### Problem: "Agent not responding"
**Solution**: Verify API key is valid and has credits

### Problem: "Deployment failed"
**Solution**: Run `az login` to authenticate with Azure

### Problem: "Slow response times"
**Solution**: Reduce `max_tokens` or use faster model

## 📚 Additional Resources

- [Full Documentation](README.md)
- [API Reference](docs/api.md)
- [Architecture Guide](docs/architecture.md)
- [Best Practices](docs/best-practices.md)

## 💡 Pro Tips

1. **Start Simple**: Begin with single agent, add complexity gradually
2. **Test Early**: Use evaluation harness from day one
3. **Version Control**: Save project exports to Git
4. **Monitor Costs**: Track token usage in sandbox metrics
5. **Use Templates**: Leverage pre-built templates as starting points

## 🎉 Next Steps

Once you're comfortable with the basics:

1. Explore advanced agent types (Team Manager, Hierarchical)
2. Integrate custom tools and functions
3. Set up automated testing in CI/CD
4. Deploy to production with monitoring
5. Share your agent templates with the community

---

**Need Help?** Open an issue or join our discussions!
