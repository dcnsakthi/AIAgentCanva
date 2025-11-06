# MAF Agent Builder - Usage Examples

## 📚 Table of Contents
1. [Basic Examples](#basic-examples)
2. [Advanced Examples](#advanced-examples)
3. [Integration Examples](#integration-examples)
4. [Deployment Examples](#deployment-examples)

---

## Basic Examples

### Example 1: Simple Customer Support Agent

**Description**: Create a single agent that handles customer inquiries.

**Steps**:
1. Login with Demo Mode
2. Create New Project:
   - Name: "Customer Support Agent"
   - Description: "A helpful agent that answers customer questions about our products"
   - Type: Single Agent
   - Complexity: Simple

3. Canvas Configuration:
   ```yaml
   Agent Type: Assistant
   Model: GPT-3.5-Turbo
   Temperature: 0.7
   System Prompt: "You are a friendly customer support agent. Help customers with product questions, troubleshooting, and general inquiries. Be polite and concise."
   Tools: None
   Vector DB: ChromaDB (for FAQ knowledge base)
   ```

4. Test in Sandbox:
   ```
   User: "How do I reset my password?"
   Agent: "I'd be happy to help you reset your password! Here's what you need to do..."
   ```

**Use Case**: Small businesses needing basic customer support automation.

---

### Example 2: Research Assistant

**Description**: Create an agent that researches topics and summarizes findings.

**Steps**:
1. Create New Project:
   - Name: "Research Assistant"
   - Description: "An agent that researches topics, finds relevant information, and creates comprehensive summaries"
   - Type: Single Agent
   - Complexity: Moderate

2. Canvas Configuration:
   ```yaml
   Agent Type: Researcher
   Model: GPT-4
   Temperature: 0.5
   System Prompt: "You are a thorough research assistant. When given a topic, search for relevant information, analyze sources, and provide well-structured summaries with citations."
   Tools: Web Search, Document Processing
   Vector DB: FAISS
   ```

3. Create Evaluation Test:
   ```yaml
   Test Name: "Research Quality Test"
   Conversation:
     - User: "Research the latest trends in AI agent frameworks"
     - Expected: Response includes multiple sources and structured summary
   Assertions:
     - Contains: "framework"
     - Length > 500 characters
   ```

**Use Case**: Academic research, market analysis, competitive intelligence.

---

### Example 3: Code Review Agent

**Description**: An agent that reviews code and provides feedback.

**Steps**:
1. Create New Project:
   - Name: "Code Reviewer"
   - Description: "Reviews Python code for bugs, performance issues, and best practices"
   - Type: Single Agent
   - Complexity: Moderate

2. Canvas Configuration:
   ```yaml
   Agent Type: Coder
   Model: GPT-4
   Temperature: 0.3
   System Prompt: "You are an expert code reviewer. Analyze code for bugs, security issues, performance problems, and adherence to best practices. Provide specific, actionable feedback."
   Tools: Code Execution
   Vector DB: None
   ```

3. Example Usage:
   ```python
   User: "Review this function:
   def calculate_total(items):
       total = 0
       for i in range(len(items)):
           total = total + items[i]['price']
       return total
   "
   
   Agent: "Here's my review:
   1. Consider using enumerate or direct iteration
   2. Use += operator for clarity
   3. Add error handling for missing 'price' key
   
   Improved version:
   def calculate_total(items):
       return sum(item.get('price', 0) for item in items)
   "
   ```

**Use Case**: Code quality assurance, developer training, automated PR reviews.

---

## Advanced Examples

### Example 4: Multi-Agent Customer Service Team

**Description**: A team of specialized agents working together.

**Agent Structure**:
```
Team Manager (Coordinator)
    ├── Triage Agent (Initial classification)
    ├── Technical Support Agent (Technical issues)
    ├── Billing Agent (Payment/billing questions)
    └── Escalation Agent (Complex cases)
```

**Implementation**:

1. **Team Manager Configuration**:
   ```yaml
   Name: "Support Coordinator"
   Type: Team Manager
   Model: GPT-4
   System Prompt: "You coordinate a customer support team. Analyze requests and delegate to the appropriate specialist: Technical Support, Billing, or Escalation."
   ```

2. **Triage Agent**:
   ```yaml
   Name: "Triage Agent"
   Type: Assistant
   Model: GPT-3.5-Turbo
   System Prompt: "You quickly classify customer inquiries into: Technical, Billing, General, or Escalation."
   ```

3. **Technical Support Agent**:
   ```yaml
   Name: "Tech Support"
   Type: Coder
   Model: GPT-4
   System Prompt: "You help customers with technical issues, troubleshooting, and product setup."
   Tools: Code Execution, Document Processing
   Vector DB: ChromaDB (technical documentation)
   ```

4. **Connections**:
   - User → Triage Agent
   - Triage Agent → Team Manager
   - Team Manager → [Technical/Billing/Escalation] Agent
   - Specialist Agent → User

5. **Evaluation Test Suite**:
   ```yaml
   Test 1: Technical Issue Routing
     User: "My API isn't working"
     Expected: Routed to Technical Support
     Assertion: Response contains technical solution
   
   Test 2: Billing Question Routing
     User: "How do I upgrade my plan?"
     Expected: Routed to Billing Agent
     Assertion: Response contains pricing information
   ```

**Use Case**: Medium to large businesses with diverse support needs.

---

### Example 5: Data Analysis Pipeline

**Description**: Multi-step data analysis workflow.

**Agent Structure**:
```
Data Pipeline Manager
    ├── Data Extractor (Collects data)
    ├── Data Cleaner (Preprocesses)
    ├── Data Analyzer (Statistical analysis)
    ├── Visualizer (Creates charts)
    └── Report Generator (Summarizes findings)
```

**Implementation**:

1. **Pipeline Manager**:
   ```yaml
   Name: "Data Pipeline Coordinator"
   Type: Team Manager
   System Prompt: "You orchestrate a data analysis pipeline. Coordinate extraction, cleaning, analysis, visualization, and reporting."
   ```

2. **Data Analyzer**:
   ```yaml
   Name: "Statistical Analyzer"
   Type: Data Analyst
   Model: GPT-4
   System Prompt: "You perform statistical analysis on datasets. Calculate metrics, identify trends, and detect anomalies."
   Tools: Data Analysis, Code Execution
   ```

3. **Visualizer**:
   ```yaml
   Name: "Chart Generator"
   Type: Data Analyst
   System Prompt: "You create clear, informative visualizations. Generate appropriate chart types based on data characteristics."
   Tools: Data Visualization
   ```

4. **Workflow**:
   ```
   User Request → Pipeline Manager
       → Data Extractor (gets raw data)
       → Data Cleaner (preprocesses)
       → Analyzer (statistical analysis)
       → Visualizer (creates charts)
       → Report Generator (comprehensive report)
   → User receives final report
   ```

**Use Case**: Business intelligence, data science teams, automated reporting.

---

### Example 6: Content Creation Team

**Description**: Collaborative content generation system.

**Agent Structure**:
```
Content Director
    ├── Researcher (Topic research)
    ├── Writer (Draft creation)
    ├── Editor (Quality review)
    └── SEO Specialist (Optimization)
```

**Workflow Example**:
```
User: "Create a blog post about sustainable energy"

1. Researcher:
   - Finds latest trends in sustainable energy
   - Identifies key topics: solar, wind, batteries
   - Collects statistics and sources

2. Writer:
   - Creates draft blog post (1000 words)
   - Incorporates research findings
   - Structures with intro, body, conclusion

3. Editor:
   - Reviews for clarity and flow
   - Checks grammar and style
   - Suggests improvements

4. SEO Specialist:
   - Optimizes for keywords
   - Adds meta description
   - Suggests internal links

Final Output: Publication-ready blog post
```

**Use Case**: Marketing teams, content agencies, publishing companies.

---

## Integration Examples

### Example 7: API Integration Agent

**Description**: Agent that interacts with external APIs.

**Implementation**:
```python
# Custom tool for API integration
class APITool:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def call_api(self, endpoint, params):
        # Make API call
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            params=params,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()

# Agent configuration
{
    "name": "API Integration Agent",
    "type": "assistant",
    "system_prompt": "You help users interact with APIs. Parse requests, make API calls, and format responses.",
    "tools": ["APITool"],
    "custom_tools": [APITool("https://api.example.com", "key")]
}
```

**Use Case**: API testing, data integration, workflow automation.

---

### Example 8: Database Query Agent

**Description**: Natural language to SQL agent.

**Configuration**:
```yaml
Name: "SQL Assistant"
Type: Data Analyst
Model: GPT-4
System Prompt: "You convert natural language queries to SQL. Understand database schema and generate accurate, safe queries."
Tools: Database Query
Vector DB: FAISS (stores schema documentation)
```

**Example Interaction**:
```
User: "Show me all customers who made purchases over $1000 last month"

Agent generates SQL:
SELECT c.customer_id, c.name, SUM(o.amount) as total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY c.customer_id
HAVING total > 1000;

Agent executes and returns results in formatted table.
```

**Use Case**: Business analysts, data exploration, reporting.

---

## Deployment Examples

### Example 9: Production Deployment to Azure

**Steps**:

1. **Configure Deployment Settings**:
   ```yaml
   Subscription: "your-subscription-id"
   Resource Group: "maf-agents-prod"
   Location: "eastus"
   Environment: "Production"
   
   Container Apps:
     CPU: 1.0
     Memory: 2Gi
     Min Replicas: 2
     Max Replicas: 20
   
   Secrets:
     - OPENAI_API_KEY
     - DATABASE_CONNECTION
     - API_KEYS
   ```

2. **Generate Deployment Scripts**:
   - Select "Bicep Template"
   - Download generated files
   - Review configuration

3. **Deploy**:
   ```bash
   # Login to Azure
   az login
   
   # Deploy using generated script
   ./deploy.sh
   
   # Verify deployment
   az containerapp show \
     --name customer-support-app \
     --resource-group maf-agents-prod
   ```

4. **Configure Monitoring**:
   - Enable Application Insights
   - Set up alerts for errors
   - Configure auto-scaling rules

5. **Access Application**:
   ```
   URL: https://customer-support-app.azurecontainerapps.io
   ```

---

### Example 10: CI/CD Pipeline Integration

**GitHub Actions Workflow**:
```yaml
name: Deploy MAF Agent

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest tests/
      
      - name: Run Evaluation Suite
        run: |
          python -m src.evaluation.test_runner
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Azure
        run: |
          az deployment group create \
            --resource-group ${{ secrets.RESOURCE_GROUP }} \
            --template-file deployment/main.bicep
```

**Use Case**: Automated testing and deployment for production agents.

---

## 🎯 Key Takeaways

1. **Start Simple**: Begin with single-agent projects
2. **Test Thoroughly**: Use evaluation harness before deployment
3. **Scale Gradually**: Add agents and complexity as needed
4. **Monitor Performance**: Track metrics in production
5. **Iterate**: Refine prompts and configurations based on results

## 📞 Need Help?

- Review QUICKSTART.md for getting started
- Check README.md for detailed documentation
- Explore PROJECT_SUMMARY.md for architecture details
