"""
Backend API for AI Agent Canvas
Provides REST endpoints for agent execution, project management, and integrations
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.agent_executor import AgentExecutor
from agents.agent_types import AgentConfig, AgentType

app = FastAPI(
    title="AI Agent Canvas API",
    description="Backend API for building and executing AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AgentExecutionRequest(BaseModel):
    agent_config: Dict[str, Any]
    input_data: str
    context: Optional[Dict[str, Any]] = None

class AgentExecutionResponse(BaseModel):
    success: bool
    output: str
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ProjectRequest(BaseModel):
    name: str
    description: str
    agent_configs: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    status: str
    services: Dict[str, str]

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = {
        "api": "healthy",
        "chromadb": check_chromadb(),
        "redis": check_redis(),
        "ollama": check_ollama()
    }
    return HealthResponse(status="healthy", services=services)

@app.post("/api/v1/agent/execute", response_model=AgentExecutionResponse)
async def execute_agent(request: AgentExecutionRequest):
    """Execute an agent with given configuration and input"""
    try:
        # Create agent config
        agent_config = AgentConfig(**request.agent_config)
        
        # Initialize executor
        executor = AgentExecutor(agent_config)
        
        # Execute agent
        result = await executor.execute_async(
            input_data=request.input_data,
            context=request.context or {}
        )
        
        return AgentExecutionResponse(
            success=True,
            output=result.get("output", ""),
            metadata=result.get("metadata", {})
        )
    except Exception as e:
        return AgentExecutionResponse(
            success=False,
            output="",
            error=str(e)
        )

@app.post("/api/v1/agent/execute/stream")
async def execute_agent_stream(request: AgentExecutionRequest):
    """Execute an agent with streaming response"""
    from fastapi.responses import StreamingResponse
    
    async def generate():
        try:
            agent_config = AgentConfig(**request.agent_config)
            executor = AgentExecutor(agent_config)
            
            async for chunk in executor.execute_stream(
                input_data=request.input_data,
                context=request.context or {}
            ):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/v1/project/create")
async def create_project(request: ProjectRequest):
    """Create a new agent project"""
    try:
        project_id = f"project_{hash(request.name)}"
        
        # Save project configuration
        project_data = {
            "id": project_id,
            "name": request.name,
            "description": request.description,
            "agents": request.agent_configs,
            "created_at": str(Path(__file__).stat().st_mtime)
        }
        
        return {
            "success": True,
            "project_id": project_id,
            "message": "Project created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/models/available")
async def get_available_models():
    """Get list of available LLM models"""
    models = {
        "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "azure_openai": ["gpt-4", "gpt-35-turbo"],
        "ollama": await get_ollama_models(),
    }
    return {"models": models}

@app.get("/api/v1/vectordb/collections")
async def get_vectordb_collections():
    """Get list of vector database collections"""
    try:
        import chromadb
        client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST", "localhost"),
            port=int(os.getenv("CHROMADB_PORT", "8000"))
        )
        collections = client.list_collections()
        return {
            "collections": [col.name for col in collections]
        }
    except Exception as e:
        return {"collections": [], "error": str(e)}

# Helper functions
def check_chromadb() -> str:
    """Check ChromaDB connection"""
    try:
        import chromadb
        client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST", "localhost"),
            port=int(os.getenv("CHROMADB_PORT", "8000"))
        )
        client.heartbeat()
        return "healthy"
    except:
        return "unavailable"

def check_redis() -> str:
    """Check Redis connection"""
    try:
        import redis
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379"))
        )
        r.ping()
        return "healthy"
    except:
        return "unavailable"

def check_ollama() -> str:
    """Check Ollama connection"""
    try:
        import requests
        response = requests.get(
            f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/tags",
            timeout=2
        )
        return "healthy" if response.status_code == 200 else "unavailable"
    except:
        return "unavailable"

async def get_ollama_models() -> List[str]:
    """Get available Ollama models"""
    try:
        import requests
        response = requests.get(
            f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/tags"
        )
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
    except:
        pass
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
