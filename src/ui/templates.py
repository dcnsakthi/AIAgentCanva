"""
Pre-built templates and playbooks for AI Agent Canvas
"""
from typing import Dict, Any, List
from datetime import datetime

class AgentTemplate:
    """Template library for pre-built agent solutions"""
    
    @staticmethod
    def get_all_templates() -> List[Dict[str, Any]]:
        """Get all available templates"""
        return [
            AgentTemplate.customer_support_team(),
            AgentTemplate.research_assistant(),
            AgentTemplate.code_review_pipeline(),
            AgentTemplate.data_analysis_workflow(),
            AgentTemplate.content_creation_team(),
            AgentTemplate.sales_automation_system(),
            AgentTemplate.hr_recruitment_assistant(),
            AgentTemplate.financial_analysis_team(),
            AgentTemplate.legal_document_reviewer(),
            AgentTemplate.marketing_campaign_manager(),
            AgentTemplate.incident_response_team(),
            AgentTemplate.ecommerce_support_system()
        ]
    
    @staticmethod
    def customer_support_team() -> Dict[str, Any]:
        """Multi-agent customer support system"""
        return {
            'id': 'customer_support_team',
            'name': 'Customer Support Team',
            'category': 'Customer Service',
            'description': 'Multi-agent system with triage, support, and escalation agents',
            'icon': '🎧',
            'complexity': 'Moderate',
            'agents_count': 3,
            'use_cases': ['Customer inquiries', 'Issue resolution', 'Escalation management'],
            'tags': ['support', 'multi-agent', 'customer-service'],
            'agents': [
                {
                    'id': 'triage_agent',
                    'name': 'Triage Agent',
                    'type': 'team_manager',
                    'role': 'Routes customer inquiries to appropriate handlers',
                    'system_prompt': 'You are a triage agent that categorizes and routes customer inquiries. Analyze the customer question and determine which specialist should handle it.',
                    'position': {'x': 100, 'y': 100}
                },
                {
                    'id': 'support_agent',
                    'name': 'Support Specialist',
                    'type': 'assistant',
                    'role': 'Handles general customer support questions',
                    'system_prompt': 'You are a friendly customer support specialist. Provide clear, helpful answers to customer questions. Be empathetic and solution-oriented.',
                    'position': {'x': 400, 'y': 100}
                },
                {
                    'id': 'escalation_agent',
                    'name': 'Escalation Manager',
                    'type': 'assistant',
                    'role': 'Handles complex issues requiring higher authority',
                    'system_prompt': 'You are an escalation manager handling complex customer issues. Provide detailed analysis and propose solutions for difficult cases.',
                    'position': {'x': 400, 'y': 300}
                }
            ],
            'connections': [
                {'from': 'triage_agent', 'to': 'support_agent', 'type': 'conditional'},
                {'from': 'triage_agent', 'to': 'escalation_agent', 'type': 'conditional'}
            ],
            'tools': ['Web Search', 'Database Query', 'Document Processing'],
            'estimated_setup_time': '15 minutes'
        }
    
    @staticmethod
    def research_assistant() -> Dict[str, Any]:
        """Single agent research assistant"""
        return {
            'id': 'research_assistant',
            'name': 'Research Assistant',
            'category': 'Research & Analysis',
            'description': 'Single agent for research, summarization, and reporting',
            'icon': '🔍',
            'complexity': 'Simple',
            'agents_count': 1,
            'use_cases': ['Academic research', 'Market analysis', 'Competitive intelligence'],
            'tags': ['research', 'single-agent', 'analysis'],
            'agents': [
                {
                    'id': 'researcher',
                    'name': 'Research Agent',
                    'type': 'researcher',
                    'role': 'Conducts comprehensive research and creates detailed reports',
                    'system_prompt': 'You are an expert research assistant. Gather information from multiple sources, synthesize findings, and create comprehensive, well-structured reports.',
                    'position': {'x': 200, 'y': 200}
                }
            ],
            'connections': [],
            'tools': ['Web Search', 'Document Processing', 'Data Analysis'],
            'estimated_setup_time': '5 minutes'
        }
    
    @staticmethod
    def code_review_pipeline() -> Dict[str, Any]:
        """Automated code review system"""
        return {
            'id': 'code_review_pipeline',
            'name': 'Code Review Pipeline',
            'category': 'Software Development',
            'description': 'Automated code analysis, testing, and review agents',
            'icon': '💻',
            'complexity': 'Complex',
            'agents_count': 4,
            'use_cases': ['Pull request reviews', 'Code quality checks', 'Security scanning'],
            'tags': ['development', 'code-review', 'automation'],
            'agents': [
                {
                    'id': 'code_analyzer',
                    'name': 'Code Analyzer',
                    'type': 'coder',
                    'role': 'Analyzes code structure and quality',
                    'system_prompt': 'You are a code quality expert. Analyze code for best practices, design patterns, and potential improvements.',
                    'position': {'x': 100, 'y': 100}
                },
                {
                    'id': 'security_scanner',
                    'name': 'Security Scanner',
                    'type': 'coder',
                    'role': 'Identifies security vulnerabilities',
                    'system_prompt': 'You are a security expert. Scan code for vulnerabilities, security issues, and compliance with security best practices.',
                    'position': {'x': 400, 'y': 100}
                },
                {
                    'id': 'test_validator',
                    'name': 'Test Validator',
                    'type': 'coder',
                    'role': 'Validates test coverage and quality',
                    'system_prompt': 'You are a testing expert. Review test coverage, suggest additional tests, and ensure test quality.',
                    'position': {'x': 100, 'y': 300}
                },
                {
                    'id': 'review_summarizer',
                    'name': 'Review Summarizer',
                    'type': 'assistant',
                    'role': 'Compiles all findings into comprehensive report',
                    'system_prompt': 'You are a technical writer. Compile code review findings into a clear, actionable report with prioritized recommendations.',
                    'position': {'x': 400, 'y': 300}
                }
            ],
            'connections': [
                {'from': 'code_analyzer', 'to': 'review_summarizer', 'type': 'sequential'},
                {'from': 'security_scanner', 'to': 'review_summarizer', 'type': 'sequential'},
                {'from': 'test_validator', 'to': 'review_summarizer', 'type': 'sequential'}
            ],
            'tools': ['Code Execution', 'Web Search', 'API Integration'],
            'estimated_setup_time': '25 minutes'
        }
    
    @staticmethod
    def data_analysis_workflow() -> Dict[str, Any]:
        """Data analysis and visualization system"""
        return {
            'id': 'data_analysis_workflow',
            'name': 'Data Analysis Workflow',
            'category': 'Data & Analytics',
            'description': 'Extract, analyze, visualize, and report on data',
            'icon': '📊',
            'complexity': 'Moderate',
            'agents_count': 3,
            'use_cases': ['Business intelligence', 'Data reporting', 'Trend analysis'],
            'tags': ['data', 'analytics', 'visualization'],
            'agents': [
                {
                    'id': 'data_extractor',
                    'name': 'Data Extractor',
                    'type': 'data_analyst',
                    'role': 'Extracts and cleans data from various sources',
                    'system_prompt': 'You are a data engineer. Extract data from various sources, clean it, and prepare it for analysis.',
                    'position': {'x': 100, 'y': 200}
                },
                {
                    'id': 'data_analyzer',
                    'name': 'Data Analyzer',
                    'type': 'data_analyst',
                    'role': 'Performs statistical analysis and identifies patterns',
                    'system_prompt': 'You are a data scientist. Analyze data to identify trends, patterns, and insights using statistical methods.',
                    'position': {'x': 300, 'y': 200}
                },
                {
                    'id': 'report_generator',
                    'name': 'Report Generator',
                    'type': 'assistant',
                    'role': 'Creates visualizations and comprehensive reports',
                    'system_prompt': 'You are a business analyst. Create clear, visual reports that communicate data insights to stakeholders.',
                    'position': {'x': 500, 'y': 200}
                }
            ],
            'connections': [
                {'from': 'data_extractor', 'to': 'data_analyzer', 'type': 'sequential'},
                {'from': 'data_analyzer', 'to': 'report_generator', 'type': 'sequential'}
            ],
            'tools': ['Data Analysis', 'Database Query', 'API Integration'],
            'estimated_setup_time': '20 minutes'
        }
    
    @staticmethod
    def content_creation_team() -> Dict[str, Any]:
        """Content creation and editing team"""
        return {
            'id': 'content_creation_team',
            'name': 'Content Creation Team',
            'category': 'Marketing & Content',
            'description': 'Collaborative team for content ideation, writing, and editing',
            'icon': '✍️',
            'complexity': 'Moderate',
            'agents_count': 3,
            'use_cases': ['Blog posts', 'Marketing copy', 'Social media content'],
            'tags': ['content', 'marketing', 'writing'],
            'agents': [
                {
                    'id': 'content_strategist',
                    'name': 'Content Strategist',
                    'type': 'assistant',
                    'role': 'Plans content strategy and outlines',
                    'system_prompt': 'You are a content strategist. Create content outlines, identify key messages, and plan content structure.',
                    'position': {'x': 100, 'y': 150}
                },
                {
                    'id': 'content_writer',
                    'name': 'Content Writer',
                    'type': 'assistant',
                    'role': 'Writes engaging content based on strategy',
                    'system_prompt': 'You are a creative content writer. Write engaging, compelling content that resonates with the target audience.',
                    'position': {'x': 300, 'y': 150}
                },
                {
                    'id': 'content_editor',
                    'name': 'Content Editor',
                    'type': 'assistant',
                    'role': 'Reviews and refines content for quality',
                    'system_prompt': 'You are an experienced editor. Review content for grammar, style, clarity, and brand consistency.',
                    'position': {'x': 500, 'y': 150}
                }
            ],
            'connections': [
                {'from': 'content_strategist', 'to': 'content_writer', 'type': 'sequential'},
                {'from': 'content_writer', 'to': 'content_editor', 'type': 'sequential'}
            ],
            'tools': ['Web Search', 'Document Processing'],
            'estimated_setup_time': '15 minutes'
        }
    
    @staticmethod
    def sales_automation_system() -> Dict[str, Any]:
        """Sales automation and lead qualification system"""
        return {
            'id': 'sales_automation_system',
            'name': 'Sales Automation System',
            'category': 'Sales & CRM',
            'description': 'Automates lead qualification, nurturing, and follow-ups',
            'icon': '💼',
            'complexity': 'Complex',
            'agents_count': 4,
            'use_cases': ['Lead qualification', 'Email automation', 'Sales analytics'],
            'tags': ['sales', 'crm', 'automation'],
            'agents': [
                {
                    'id': 'lead_qualifier',
                    'name': 'Lead Qualifier',
                    'type': 'assistant',
                    'role': 'Qualifies and scores leads',
                    'system_prompt': 'You are a sales development representative. Qualify leads based on criteria and assign scores.',
                    'position': {'x': 100, 'y': 100}
                },
                {
                    'id': 'email_composer',
                    'name': 'Email Composer',
                    'type': 'assistant',
                    'role': 'Creates personalized outreach emails',
                    'system_prompt': 'You are a sales copywriter. Create personalized, compelling sales emails that drive engagement.',
                    'position': {'x': 400, 'y': 100}
                },
                {
                    'id': 'followup_scheduler',
                    'name': 'Follow-up Scheduler',
                    'type': 'assistant',
                    'role': 'Manages follow-up sequences',
                    'system_prompt': 'You are a sales operations specialist. Plan and schedule strategic follow-ups based on lead behavior.',
                    'position': {'x': 100, 'y': 300}
                },
                {
                    'id': 'sales_analyst',
                    'name': 'Sales Analyst',
                    'type': 'data_analyst',
                    'role': 'Analyzes sales performance and provides insights',
                    'system_prompt': 'You are a sales analyst. Track metrics, identify trends, and provide actionable insights to improve sales.',
                    'position': {'x': 400, 'y': 300}
                }
            ],
            'connections': [
                {'from': 'lead_qualifier', 'to': 'email_composer', 'type': 'conditional'},
                {'from': 'email_composer', 'to': 'followup_scheduler', 'type': 'sequential'},
                {'from': 'followup_scheduler', 'to': 'sales_analyst', 'type': 'sequential'}
            ],
            'tools': ['API Integration', 'Database Query', 'Web Search'],
            'estimated_setup_time': '30 minutes'
        }
    
    @staticmethod
    def hr_recruitment_assistant() -> Dict[str, Any]:
        """HR recruitment and candidate screening system"""
        return {
            'id': 'hr_recruitment_assistant',
            'name': 'HR Recruitment Assistant',
            'category': 'Human Resources',
            'description': 'Streamlines candidate screening, interview scheduling, and evaluation',
            'icon': '👥',
            'complexity': 'Moderate',
            'agents_count': 3,
            'use_cases': ['Resume screening', 'Interview scheduling', 'Candidate evaluation'],
            'tags': ['hr', 'recruitment', 'hiring'],
            'agents': [
                {
                    'id': 'resume_screener',
                    'name': 'Resume Screener',
                    'type': 'assistant',
                    'role': 'Reviews and ranks resumes',
                    'system_prompt': 'You are an HR specialist. Review resumes, extract key qualifications, and rank candidates based on job requirements.',
                    'position': {'x': 150, 'y': 150}
                },
                {
                    'id': 'interview_coordinator',
                    'name': 'Interview Coordinator',
                    'type': 'assistant',
                    'role': 'Schedules and manages interviews',
                    'system_prompt': 'You are an interview coordinator. Schedule interviews, send invitations, and manage the interview process.',
                    'position': {'x': 350, 'y': 150}
                },
                {
                    'id': 'candidate_evaluator',
                    'name': 'Candidate Evaluator',
                    'type': 'assistant',
                    'role': 'Compiles feedback and makes recommendations',
                    'system_prompt': 'You are an HR business partner. Evaluate candidate feedback, compile assessments, and provide hiring recommendations.',
                    'position': {'x': 550, 'y': 150}
                }
            ],
            'connections': [
                {'from': 'resume_screener', 'to': 'interview_coordinator', 'type': 'sequential'},
                {'from': 'interview_coordinator', 'to': 'candidate_evaluator', 'type': 'sequential'}
            ],
            'tools': ['Document Processing', 'Database Query', 'API Integration'],
            'estimated_setup_time': '20 minutes'
        }
    
    @staticmethod
    def financial_analysis_team() -> Dict[str, Any]:
        """Financial analysis and reporting team"""
        return {
            'id': 'financial_analysis_team',
            'name': 'Financial Analysis Team',
            'category': 'Finance & Accounting',
            'description': 'Analyzes financial data and generates comprehensive reports',
            'icon': '💰',
            'complexity': 'Complex',
            'agents_count': 3,
            'use_cases': ['Financial reporting', 'Budget analysis', 'Forecasting'],
            'tags': ['finance', 'accounting', 'analysis'],
            'agents': [
                {
                    'id': 'data_collector',
                    'name': 'Financial Data Collector',
                    'type': 'data_analyst',
                    'role': 'Collects and validates financial data',
                    'system_prompt': 'You are a financial data analyst. Collect financial data from various sources and validate its accuracy.',
                    'position': {'x': 100, 'y': 200}
                },
                {
                    'id': 'financial_analyst',
                    'name': 'Financial Analyst',
                    'type': 'data_analyst',
                    'role': 'Performs financial analysis and modeling',
                    'system_prompt': 'You are a financial analyst. Analyze financial statements, perform ratio analysis, and create financial models.',
                    'position': {'x': 350, 'y': 200}
                },
                {
                    'id': 'report_writer',
                    'name': 'Financial Report Writer',
                    'type': 'assistant',
                    'role': 'Creates executive financial reports',
                    'system_prompt': 'You are a financial reporting specialist. Create clear, comprehensive financial reports for executives and stakeholders.',
                    'position': {'x': 600, 'y': 200}
                }
            ],
            'connections': [
                {'from': 'data_collector', 'to': 'financial_analyst', 'type': 'sequential'},
                {'from': 'financial_analyst', 'to': 'report_writer', 'type': 'sequential'}
            ],
            'tools': ['Data Analysis', 'Database Query', 'API Integration'],
            'estimated_setup_time': '25 minutes'
        }
    
    @staticmethod
    def legal_document_reviewer() -> Dict[str, Any]:
        """Legal document review and analysis system"""
        return {
            'id': 'legal_document_reviewer',
            'name': 'Legal Document Reviewer',
            'category': 'Legal & Compliance',
            'description': 'Reviews contracts and legal documents for risks and compliance',
            'icon': '⚖️',
            'complexity': 'Complex',
            'agents_count': 2,
            'use_cases': ['Contract review', 'Compliance checking', 'Risk assessment'],
            'tags': ['legal', 'compliance', 'contracts'],
            'agents': [
                {
                    'id': 'document_analyzer',
                    'name': 'Document Analyzer',
                    'type': 'assistant',
                    'role': 'Analyzes legal documents and identifies key clauses',
                    'system_prompt': 'You are a legal analyst. Review legal documents, identify key clauses, and flag potential issues or risks.',
                    'position': {'x': 200, 'y': 200}
                },
                {
                    'id': 'compliance_checker',
                    'name': 'Compliance Checker',
                    'type': 'assistant',
                    'role': 'Verifies compliance with regulations',
                    'system_prompt': 'You are a compliance specialist. Check documents for regulatory compliance and identify any violations or concerns.',
                    'position': {'x': 500, 'y': 200}
                }
            ],
            'connections': [
                {'from': 'document_analyzer', 'to': 'compliance_checker', 'type': 'sequential'}
            ],
            'tools': ['Document Processing', 'Web Search', 'Database Query'],
            'estimated_setup_time': '20 minutes'
        }
    
    @staticmethod
    def marketing_campaign_manager() -> Dict[str, Any]:
        """Marketing campaign planning and execution system"""
        return {
            'id': 'marketing_campaign_manager',
            'name': 'Marketing Campaign Manager',
            'category': 'Marketing & Content',
            'description': 'Plans, executes, and analyzes marketing campaigns',
            'icon': '📱',
            'complexity': 'Complex',
            'agents_count': 4,
            'use_cases': ['Campaign planning', 'Content creation', 'Performance tracking'],
            'tags': ['marketing', 'campaigns', 'analytics'],
            'agents': [
                {
                    'id': 'campaign_strategist',
                    'name': 'Campaign Strategist',
                    'type': 'assistant',
                    'role': 'Develops campaign strategy and goals',
                    'system_prompt': 'You are a marketing strategist. Develop comprehensive campaign strategies with clear goals and target audiences.',
                    'position': {'x': 100, 'y': 100}
                },
                {
                    'id': 'content_creator',
                    'name': 'Content Creator',
                    'type': 'assistant',
                    'role': 'Creates campaign content and assets',
                    'system_prompt': 'You are a creative content creator. Produce engaging marketing content across various channels.',
                    'position': {'x': 400, 'y': 100}
                },
                {
                    'id': 'channel_manager',
                    'name': 'Channel Manager',
                    'type': 'assistant',
                    'role': 'Manages distribution across channels',
                    'system_prompt': 'You are a channel manager. Coordinate content distribution across email, social media, and other channels.',
                    'position': {'x': 100, 'y': 300}
                },
                {
                    'id': 'performance_analyst',
                    'name': 'Performance Analyst',
                    'type': 'data_analyst',
                    'role': 'Tracks and analyzes campaign performance',
                    'system_prompt': 'You are a marketing analyst. Track campaign metrics, analyze performance, and provide optimization recommendations.',
                    'position': {'x': 400, 'y': 300}
                }
            ],
            'connections': [
                {'from': 'campaign_strategist', 'to': 'content_creator', 'type': 'sequential'},
                {'from': 'content_creator', 'to': 'channel_manager', 'type': 'sequential'},
                {'from': 'channel_manager', 'to': 'performance_analyst', 'type': 'sequential'}
            ],
            'tools': ['API Integration', 'Data Analysis', 'Web Search'],
            'estimated_setup_time': '30 minutes'
        }
    
    @staticmethod
    def incident_response_team() -> Dict[str, Any]:
        """IT incident response and resolution system"""
        return {
            'id': 'incident_response_team',
            'name': 'Incident Response Team',
            'category': 'IT & Operations',
            'description': 'Manages and resolves IT incidents and service requests',
            'icon': '🚨',
            'complexity': 'Complex',
            'agents_count': 4,
            'use_cases': ['Incident triage', 'Root cause analysis', 'Resolution tracking'],
            'tags': ['it', 'operations', 'incident-management'],
            'agents': [
                {
                    'id': 'incident_triage',
                    'name': 'Incident Triage',
                    'type': 'team_manager',
                    'role': 'Triages and prioritizes incidents',
                    'system_prompt': 'You are an IT triage specialist. Categorize incidents, assess severity, and route to appropriate teams.',
                    'position': {'x': 100, 'y': 100}
                },
                {
                    'id': 'technical_analyst',
                    'name': 'Technical Analyst',
                    'type': 'coder',
                    'role': 'Investigates technical issues',
                    'system_prompt': 'You are a technical analyst. Investigate incidents, analyze logs, and identify root causes.',
                    'position': {'x': 400, 'y': 100}
                },
                {
                    'id': 'resolution_specialist',
                    'name': 'Resolution Specialist',
                    'type': 'assistant',
                    'role': 'Implements fixes and workarounds',
                    'system_prompt': 'You are a resolution specialist. Implement fixes, test solutions, and document resolutions.',
                    'position': {'x': 100, 'y': 300}
                },
                {
                    'id': 'communication_manager',
                    'name': 'Communication Manager',
                    'type': 'assistant',
                    'role': 'Manages stakeholder communications',
                    'system_prompt': 'You are a communication manager. Keep stakeholders informed with clear, timely incident updates.',
                    'position': {'x': 400, 'y': 300}
                }
            ],
            'connections': [
                {'from': 'incident_triage', 'to': 'technical_analyst', 'type': 'conditional'},
                {'from': 'technical_analyst', 'to': 'resolution_specialist', 'type': 'sequential'},
                {'from': 'resolution_specialist', 'to': 'communication_manager', 'type': 'parallel'}
            ],
            'tools': ['API Integration', 'Database Query', 'Code Execution'],
            'estimated_setup_time': '30 minutes'
        }
    
    @staticmethod
    def ecommerce_support_system() -> Dict[str, Any]:
        """E-commerce customer support and order management"""
        return {
            'id': 'ecommerce_support_system',
            'name': 'E-commerce Support System',
            'category': 'E-commerce',
            'description': 'Handles orders, returns, and customer inquiries for online stores',
            'icon': '🛒',
            'complexity': 'Moderate',
            'agents_count': 3,
            'use_cases': ['Order tracking', 'Return processing', 'Product inquiries'],
            'tags': ['ecommerce', 'retail', 'customer-service'],
            'agents': [
                {
                    'id': 'order_assistant',
                    'name': 'Order Assistant',
                    'type': 'assistant',
                    'role': 'Handles order-related inquiries',
                    'system_prompt': 'You are an order specialist. Help customers track orders, modify shipments, and resolve order issues.',
                    'position': {'x': 150, 'y': 150}
                },
                {
                    'id': 'product_advisor',
                    'name': 'Product Advisor',
                    'type': 'assistant',
                    'role': 'Provides product recommendations',
                    'system_prompt': 'You are a product expert. Answer product questions, provide recommendations, and help customers make informed decisions.',
                    'position': {'x': 400, 'y': 150}
                },
                {
                    'id': 'returns_specialist',
                    'name': 'Returns Specialist',
                    'type': 'assistant',
                    'role': 'Processes returns and refunds',
                    'system_prompt': 'You are a returns specialist. Process return requests, issue refunds, and handle exchange transactions.',
                    'position': {'x': 650, 'y': 150}
                }
            ],
            'connections': [
                {'from': 'order_assistant', 'to': 'product_advisor', 'type': 'conditional'},
                {'from': 'order_assistant', 'to': 'returns_specialist', 'type': 'conditional'}
            ],
            'tools': ['API Integration', 'Database Query', 'Web Search'],
            'estimated_setup_time': '20 minutes'
        }
    
    @staticmethod
    def get_template_by_id(template_id: str) -> Dict[str, Any]:
        """Get specific template by ID"""
        templates = AgentTemplate.get_all_templates()
        for template in templates:
            if template['id'] == template_id:
                return template
        return None
    
    @staticmethod
    def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
        """Get templates filtered by category"""
        templates = AgentTemplate.get_all_templates()
        return [t for t in templates if t['category'] == category]
    
    @staticmethod
    def get_templates_by_complexity(complexity: str) -> List[Dict[str, Any]]:
        """Get templates filtered by complexity"""
        templates = AgentTemplate.get_all_templates()
        return [t for t in templates if t['complexity'] == complexity]
    
    @staticmethod
    def search_templates(query: str) -> List[Dict[str, Any]]:
        """Search templates by name, description, or tags"""
        templates = AgentTemplate.get_all_templates()
        query = query.lower()
        return [
            t for t in templates
            if query in t['name'].lower()
            or query in t['description'].lower()
            or any(query in tag for tag in t['tags'])
        ]
    
    @staticmethod
    def load_template_as_project(template: Dict[str, Any]) -> Dict[str, Any]:
        """Convert template to project format"""
        return {
            'id': f"project_{datetime.now().timestamp()}",
            'name': template['name'],
            'description': template['description'],
            'category': template.get('category', 'General'),
            'complexity': template.get('complexity', 'Moderate'),
            'agents': template.get('agents', []),
            'connections': template.get('connections', []),
            'tools': template.get('tools', []),
            'created_at': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat(),
            'from_template': template['id']
        }
