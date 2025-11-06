"""
Agent types and factory for creating different agent types
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    """Available agent types"""
    ASSISTANT = "assistant"
    RESEARCHER = "researcher"
    CODER = "coder"
    DATA_ANALYST = "data_analyst"
    TEAM_MANAGER = "team_manager"

@dataclass
class AgentConfig:
    """Configuration for an agent"""
    id: str
    name: str
    type: AgentType
    system_prompt: str
    llm_model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    tools: List[str] = None
    vector_db: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []
        if self.metadata is None:
            self.metadata = {}

class AgentFactory:
    """Factory for creating agents"""
    
    @staticmethod
    def create_agent(config: AgentConfig) -> 'BaseAgent':
        """Create an agent based on configuration"""
        
        if config.type == AgentType.ASSISTANT:
            from src.agents.implementations.assistant_agent import AssistantAgent
            return AssistantAgent(config)
        
        elif config.type == AgentType.RESEARCHER:
            from src.agents.implementations.researcher_agent import ResearcherAgent
            return ResearcherAgent(config)
        
        elif config.type == AgentType.CODER:
            from src.agents.implementations.coder_agent import CoderAgent
            return CoderAgent(config)
        
        elif config.type == AgentType.DATA_ANALYST:
            from src.agents.implementations.data_analyst_agent import DataAnalystAgent
            return DataAnalystAgent(config)
        
        elif config.type == AgentType.TEAM_MANAGER:
            from src.agents.implementations.team_manager_agent import TeamManagerAgent
            return TeamManagerAgent(config)
        
        else:
            raise ValueError(f"Unknown agent type: {config.type}")
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BaseAgent':
        """Create agent from dictionary"""
        
        config = AgentConfig(
            id=data['id'],
            name=data['name'],
            type=AgentType(data['type']),
            system_prompt=data.get('system_prompt', ''),
            llm_model=data.get('llm_model', 'gpt-4'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 1000),
            tools=data.get('tools', []),
            vector_db=data.get('vector_db'),
            metadata=data.get('metadata', {})
        )
        
        return AgentFactory.create_agent(config)

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.id = config.id
        self.name = config.name
        self.type = config.type
        self.system_prompt = config.system_prompt
        self.llm_model = config.llm_model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        self.tools = config.tools
        self.vector_db = config.vector_db
        self.metadata = config.metadata
    
    async def execute(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute agent with a message"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def get_config(self) -> Dict[str, Any]:
        """Get agent configuration as dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'system_prompt': self.system_prompt,
            'llm_model': self.llm_model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'tools': self.tools,
            'vector_db': self.vector_db,
            'metadata': self.metadata
        }
