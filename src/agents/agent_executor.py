"""
Agent executor - Runs agents with LLM providers
"""
from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime

# Optional imports for production mode
try:
    import openai
except ImportError:
    openai = None

try:
    from azure.identity import DefaultAzureCredential
except ImportError:
    DefaultAzureCredential = None

from src.utils.config_loader import ConfigLoader
from src.agents.agent_types import AgentFactory

class AgentExecutor:
    """Executes agents with configured LLM providers"""
    
    def __init__(self, project: Dict[str, Any]):
        self.project = project
        self.config = ConfigLoader.load_config()
        self.agents = {}
        
        # Initialize agents
        for agent_data in project.get('agents', []):
            try:
                agent = AgentFactory.from_dict(agent_data)
                self.agents[agent.id] = agent
            except Exception as e:
                print(f"Error loading agent {agent_data.get('id')}: {e}")
    
    def run_agent(self, agent_id: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run an agent synchronously"""
        
        if agent_id not in self.agents:
            return {
                'success': False,
                'error': f"Agent {agent_id} not found"
            }
        
        agent = self.agents[agent_id]
        
        try:
            # Get LLM provider
            llm_response = self._call_llm(
                model=agent.llm_model,
                messages=[
                    {"role": "system", "content": agent.system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=agent.temperature,
                max_tokens=agent.max_tokens
            )
            
            return {
                'success': True,
                'response': llm_response['content'],
                'tokens_used': llm_response['tokens'],
                'model': agent.llm_model
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def run_agent_async(self, agent_id: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run an agent asynchronously"""
        
        if agent_id not in self.agents:
            return {
                'success': False,
                'error': f"Agent {agent_id} not found"
            }
        
        agent = self.agents[agent_id]
        
        try:
            result = await agent.execute(message, context)
            return result
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _call_llm(self, model: str, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Call LLM provider"""
        
        # Determine provider from model name
        if 'gpt' in model.lower():
            return self._call_openai(model, messages, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    def _call_openai(self, model: str, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Call OpenAI or Azure OpenAI"""
        
        # Check if in demo mode
        api_key = ConfigLoader.get_env("OPENAI_API_KEY")
        if api_key == "demo-mode" or ConfigLoader.get_env("APP_ENV") == "demo":
            # Demo mode - return simulated response
            import random
            user_message = messages[-1]['content'] if messages else ""
            system_prompt = next((m['content'] for m in messages if m['role'] == 'system'), "")
            
            # Generate contextual demo response
            demo_responses = [
                f"Thank you for your question about '{user_message[:50]}...'. Based on my understanding, here's what I can help you with:\n\n1. I've analyzed your request carefully\n2. I can provide detailed information on this topic\n3. Let me guide you through the solution step by step\n\nThis is a demo response showing how the agent would interact with you. In production, this would be powered by {model}.",
                
                f"I understand you're asking about: '{user_message[:50]}...'\n\nHere's my analysis:\n- This is an interesting question that requires careful consideration\n- Based on the context, I recommend the following approach\n- Let's break this down into manageable steps\n\nNote: This is a demonstration response. The actual agent would use {model} to provide real-time, intelligent responses.",
                
                f"Great question! Regarding '{user_message[:50]}...', I can help with that.\n\nKey points to consider:\n• Understanding the requirements\n• Evaluating different approaches\n• Implementing the best solution\n• Testing and validation\n\nThis demo showcases the agent's capabilities. In production mode, responses would be generated by {model} with real-time intelligence."
            ]
            
            response_content = random.choice(demo_responses)
            estimated_tokens = len(response_content.split()) * 1.3
            
            return {
                'content': response_content,
                'tokens': int(estimated_tokens),
                'finish_reason': 'stop'
            }
        
        # Check if using Azure OpenAI
        azure_endpoint = ConfigLoader.get_env("AZURE_OPENAI_ENDPOINT")
        azure_api_key = ConfigLoader.get_env("AZURE_OPENAI_API_KEY")
        
        if azure_endpoint and azure_api_key and azure_endpoint != "demo-mode":
            # Azure OpenAI
            client = openai.AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                api_version=ConfigLoader.get_env("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
            )
            
            deployment_name = ConfigLoader.get_env("AZURE_OPENAI_DEPLOYMENT_NAME", model)
            
            response = client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            # Standard OpenAI
            if not api_key:
                raise ValueError("No OpenAI API key configured")
            
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        return {
            'content': response.choices[0].message.content,
            'tokens': response.usage.total_tokens,
            'finish_reason': response.choices[0].finish_reason
        }
    
    def run_multi_agent(self, agent_ids: List[str], message: str) -> List[Dict[str, Any]]:
        """Run multiple agents in parallel"""
        
        results = []
        
        for agent_id in agent_ids:
            result = self.run_agent(agent_id, message)
            results.append({
                'agent_id': agent_id,
                'agent_name': self.agents[agent_id].name if agent_id in self.agents else 'Unknown',
                'result': result
            })
        
        return results
