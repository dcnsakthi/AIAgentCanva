"""
Test case definition
"""
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

class AssertionType(Enum):
    """Types of assertions"""
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    EQUALS = "equals"
    MATCHES_REGEX = "matches_regex"
    LENGTH_GT = "length_greater_than"
    LENGTH_LT = "length_less_than"

@dataclass
class Assertion:
    """Test assertion"""
    type: AssertionType
    value: str
    description: str = ""

@dataclass
class ConversationTurn:
    """Single turn in conversation"""
    role: str  # "user" or "assistant"
    content: str

@dataclass
class TestCase:
    """Test case for agent evaluation"""
    id: str
    name: str
    description: str
    agent_id: str
    conversation: List[ConversationTurn]
    assertions: List[Assertion]
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'agent_id': self.agent_id,
            'conversation': [
                {'role': turn.role, 'content': turn.content}
                for turn in self.conversation
            ],
            'assertions': [
                {'type': assertion.type.value, 'value': assertion.value, 'description': assertion.description}
                for assertion in self.assertions
            ],
            'metadata': self.metadata or {}
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TestCase':
        """Create from dictionary"""
        return TestCase(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            agent_id=data['agent_id'],
            conversation=[
                ConversationTurn(role=turn['role'], content=turn['content'])
                for turn in data['conversation']
            ],
            assertions=[
                Assertion(
                    type=AssertionType(assertion['type']),
                    value=assertion['value'],
                    description=assertion.get('description', '')
                )
                for assertion in data['assertions']
            ],
            metadata=data.get('metadata', {})
        )
