# AI Agent Templates

This directory contains pre-built templates and playbooks for common AI agent scenarios.

## Overview

The template system provides ready-to-use agent configurations for various business use cases. Each template includes:

- **Pre-configured agents** with specialized roles and system prompts
- **Agent connections** defining workflow and communication patterns
- **Recommended tools** for the specific use case
- **Use case descriptions** and example scenarios

## Available Templates

### 1. Customer Service
- **Customer Support Team** - Multi-agent triage, support, and escalation system
- **E-commerce Support System** - Order tracking, returns, and product inquiries

### 2. Research & Analysis
- **Research Assistant** - Comprehensive research and reporting
- **Financial Analysis Team** - Financial data analysis and reporting

### 3. Software Development
- **Code Review Pipeline** - Automated code analysis, security scanning, and testing
- **Incident Response Team** - IT incident management and resolution

### 4. Data & Analytics
- **Data Analysis Workflow** - ETL, analysis, and visualization pipeline

### 5. Marketing & Content
- **Content Creation Team** - Strategy, writing, and editing workflow
- **Marketing Campaign Manager** - Campaign planning and execution

### 6. Sales & CRM
- **Sales Automation System** - Lead qualification and nurturing

### 7. Human Resources
- **HR Recruitment Assistant** - Resume screening and interview coordination

### 8. Legal & Compliance
- **Legal Document Reviewer** - Contract review and compliance checking

## Template Structure

Each template follows this structure:

```python
{
    'id': 'unique_template_id',
    'name': 'Display Name',
    'category': 'Category Name',
    'description': 'Brief description',
    'icon': '🎯',
    'complexity': 'Simple|Moderate|Complex|Enterprise',
    'agents_count': 3,
    'use_cases': ['Use case 1', 'Use case 2'],
    'tags': ['tag1', 'tag2'],
    'agents': [
        {
            'id': 'agent_id',
            'name': 'Agent Name',
            'type': 'agent_type',
            'role': 'Agent role description',
            'system_prompt': 'System prompt for the agent',
            'position': {'x': 100, 'y': 100}
        }
    ],
    'connections': [
        {
            'from': 'agent1_id',
            'to': 'agent2_id',
            'type': 'sequential|parallel|conditional'
        }
    ],
    'tools': ['Tool 1', 'Tool 2'],
    'estimated_setup_time': '15 minutes'
}
```

## Using Templates

### In the UI

1. Go to the **Templates** tab on the landing page
2. Browse or search for templates
3. Filter by category or complexity
4. Click "View Details" to see full template information
5. Click "Use This Template" to load it into the canvas

### Programmatically

```python
from src.ui.templates import AgentTemplate

# Get all templates
templates = AgentTemplate.get_all_templates()

# Get specific template
template = AgentTemplate.get_template_by_id('customer_support_team')

# Filter by category
support_templates = AgentTemplate.get_templates_by_category('Customer Service')

# Filter by complexity
simple_templates = AgentTemplate.get_templates_by_complexity('Simple')

# Search templates
results = AgentTemplate.search_templates('customer support')

# Load template as project
project = AgentTemplate.load_template_as_project(template)
```

## Creating Custom Templates

To add a new template:

1. Open `src/ui/templates.py`
2. Add a new static method to the `AgentTemplate` class
3. Follow the template structure outlined above
4. Add the method to the `get_all_templates()` list
5. Update the category in `config.yaml` if needed

### Example

```python
@staticmethod
def my_custom_template() -> Dict[str, Any]:
    """My custom agent template"""
    return {
        'id': 'my_custom_template',
        'name': 'My Custom Template',
        'category': 'Custom Category',
        'description': 'Description of what this template does',
        'icon': '🎯',
        'complexity': 'Moderate',
        'agents_count': 2,
        'use_cases': ['Use case 1', 'Use case 2'],
        'tags': ['custom', 'example'],
        'agents': [
            # Define your agents here
        ],
        'connections': [
            # Define connections here
        ],
        'tools': ['Tool 1', 'Tool 2'],
        'estimated_setup_time': '10 minutes'
    }
```

## Template Categories

- **Customer Service** - Support, help desk, and customer interaction systems
- **Research & Analysis** - Information gathering and analysis
- **Software Development** - Code-related automation and workflows
- **Data & Analytics** - Data processing and business intelligence
- **Marketing & Content** - Content creation and campaign management
- **Sales & CRM** - Sales processes and customer relationship management
- **Human Resources** - Recruitment and HR processes
- **Finance & Accounting** - Financial analysis and reporting
- **Legal & Compliance** - Legal document processing and compliance
- **IT & Operations** - IT service management and operations
- **E-commerce** - Online retail and order management

## Complexity Levels

- **Simple** - Single agent or basic multi-agent (1-2 agents)
- **Moderate** - Standard multi-agent systems (3-4 agents)
- **Complex** - Advanced multi-agent systems (5+ agents)
- **Enterprise** - Large-scale systems with multiple teams

## Best Practices

1. **Start with a template** - Use templates as starting points and customize as needed
2. **Understand the workflow** - Review the agent connections and flow before using
3. **Customize prompts** - Tailor system prompts to your specific needs
4. **Test thoroughly** - Use the evaluation tools to test template performance
5. **Document changes** - Keep track of customizations made to templates

## Configuration

Template settings can be configured in `config.yaml`:

```yaml
templates:
  enabled: true
  categories: [...]
  complexity_levels: [...]
  featured_templates: [...]
```

## Support

For questions or issues with templates:
- Review the documentation
- Check example use cases in each template
- Refer to the agent type definitions in `config.yaml`
- Contact support for custom template development
