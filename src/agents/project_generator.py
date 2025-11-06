"""
Project generator - Generate project from prompts
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class ProjectGenerator:
    """Generate agent projects from natural language prompts"""
    
    def generate_from_prompt(
        self,
        name: str,
        description: str,
        agent_type: str,
        complexity: str,
        documents: List[Dict[str, Any]],
        tools: List[str]
    ) -> Dict[str, Any]:
        """Generate a project structure from user inputs"""
        
        # Create base project
        project = {
            'id': f"project_{datetime.now().timestamp()}",
            'name': name,
            'description': description,
            'agent_type': agent_type,
            'complexity': complexity,
            'agents': [],
            'connections': [],
            'documents': documents,
            'tools': tools,
            'created_at': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
        }
        
        # Generate agents based on type
        if agent_type == "Single Agent":
            project['agents'] = self._generate_single_agent(name, description, tools)
        
        elif agent_type == "Multi-Agent Team":
            project['agents'] = self._generate_multi_agent_team(name, description, complexity, tools)
        
        elif agent_type == "Hierarchical Team":
            project['agents'] = self._generate_hierarchical_team(name, description, complexity, tools)
        
        return project
    
    def _generate_single_agent(self, name: str, description: str, tools: List[str]) -> List[Dict[str, Any]]:
        """Generate a single agent configuration"""
        
        agent = {
            'id': 'agent_0',
            'name': name,
            'type': 'assistant',
            'system_prompt': f"You are a helpful AI assistant for: {description}",
            'llm_model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 2000,
            'tools': tools,
            'vector_db': 'chromadb' if tools else None,
            'position': {'x': 200, 'y': 200}
        }
        
        return [agent]
    
    def _generate_multi_agent_team(self, name: str, description: str, complexity: str, tools: List[str]) -> List[Dict[str, Any]]:
        """Generate a multi-agent team configuration"""
        
        agents = []
        
        # Coordinator agent
        agents.append({
            'id': 'agent_coordinator',
            'name': 'Coordinator',
            'type': 'team_manager',
            'system_prompt': f"You coordinate a team of agents to: {description}",
            'llm_model': 'gpt-4',
            'temperature': 0.5,
            'max_tokens': 1500,
            'tools': [],
            'vector_db': None,
            'position': {'x': 400, 'y': 100}
        })
        
        # Specialist agents based on complexity
        num_specialists = {'Simple': 2, 'Moderate': 3, 'Complex': 4, 'Enterprise': 5}[complexity]
        
        specialist_types = [
            {'type': 'researcher', 'name': 'Research Agent', 'prompt': 'You research and gather information.'},
            {'type': 'coder', 'name': 'Code Agent', 'prompt': 'You write and analyze code.'},
            {'type': 'data_analyst', 'name': 'Analysis Agent', 'prompt': 'You analyze data and create insights.'},
            {'type': 'assistant', 'name': 'Support Agent', 'prompt': 'You provide general assistance.'},
            {'type': 'assistant', 'name': 'QA Agent', 'prompt': 'You ensure quality and accuracy.'}
        ]
        
        for i in range(min(num_specialists, len(specialist_types))):
            spec = specialist_types[i]
            agents.append({
                'id': f'agent_specialist_{i}',
                'name': spec['name'],
                'type': spec['type'],
                'system_prompt': spec['prompt'],
                'llm_model': 'gpt-4',
                'temperature': 0.7,
                'max_tokens': 1500,
                'tools': tools if i == 0 else [],
                'vector_db': 'chromadb' if i == 0 else None,
                'position': {'x': 200 + (i * 150), 'y': 300}
            })
        
        return agents
    
    def _generate_hierarchical_team(self, name: str, description: str, complexity: str, tools: List[str]) -> List[Dict[str, Any]]:
        """Generate a hierarchical team configuration"""
        
        agents = []
        
        # Top-level manager
        agents.append({
            'id': 'agent_manager',
            'name': 'Team Manager',
            'type': 'team_manager',
            'system_prompt': f"You are the lead manager for: {description}. You delegate tasks to team leads.",
            'llm_model': 'gpt-4',
            'temperature': 0.5,
            'max_tokens': 2000,
            'tools': [],
            'vector_db': None,
            'position': {'x': 400, 'y': 50}
        })
        
        # Team leads
        team_leads = [
            {'name': 'Research Lead', 'type': 'researcher', 'prompt': 'You lead the research team.'},
            {'name': 'Development Lead', 'type': 'coder', 'prompt': 'You lead the development team.'}
        ]
        
        for i, lead in enumerate(team_leads):
            agents.append({
                'id': f'agent_lead_{i}',
                'name': lead['name'],
                'type': lead['type'],
                'system_prompt': lead['prompt'],
                'llm_model': 'gpt-4',
                'temperature': 0.6,
                'max_tokens': 1500,
                'tools': tools if i == 0 else [],
                'vector_db': 'chromadb' if i == 0 else None,
                'position': {'x': 250 + (i * 300), 'y': 200}
            })
            
            # Subordinates for each lead
            for j in range(2):
                agents.append({
                    'id': f'agent_worker_{i}_{j}',
                    'name': f'{lead["name"]} Worker {j+1}',
                    'type': 'assistant',
                    'system_prompt': f'You assist the {lead["name"]}.',
                    'llm_model': 'gpt-35-turbo',
                    'temperature': 0.7,
                    'max_tokens': 1000,
                    'tools': [],
                    'vector_db': None,
                    'position': {'x': 200 + (i * 300) + (j * 100), 'y': 350}
                })
        
        return agents
