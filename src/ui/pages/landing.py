"""
Landing page - Prompt-to-canvas flow
"""
import streamlit as st
from typing import Dict, Any
import json
from datetime import datetime
from src.utils.config_loader import ConfigLoader
from src.agents.project_generator import ProjectGenerator

def show():
    """Display landing page"""
    
    st.markdown("<h1 class='main-header'>Welcome to MAF Agent Builder</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Build enterprise-grade AI agents with visual tools and Microsoft Agent Framework</p>",
               unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚀 Quick Start")
        
        # Create new project tab
        tabs = st.tabs(["📝 New Project", "📂 Load Project", "📚 Templates"])
        
        with tabs[0]:
            show_new_project_form()
        
        with tabs[1]:
            show_load_project()
        
        with tabs[2]:
            show_templates()
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        show_stats_panel()
        
        st.markdown("### 🎓 Getting Started")
        show_quick_links()

def show_new_project_form():
    """Display new project creation form"""
    
    st.markdown("#### Create Your AI Agent Solution")
    st.markdown("Describe what you want to build, and we'll generate a starting point for your canvas.")
    
    with st.form("new_project_form"):
        project_name = st.text_input(
            "Project Name",
            placeholder="e.g., Customer Support Agent System"
        )
        
        project_description = st.text_area(
            "Project Description / Product Brief",
            placeholder="Describe your agent system: What problem does it solve? What tasks should it handle? What data sources will it use?",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            agent_type = st.selectbox(
                "Primary Agent Type",
                ["Single Agent", "Multi-Agent Team", "Hierarchical Team"]
            )
        
        with col2:
            complexity = st.select_slider(
                "Complexity Level",
                options=["Simple", "Moderate", "Complex", "Enterprise"],
                value="Moderate"
            )
        
        # Document upload
        st.markdown("##### 📎 Attach Context Documents (Optional)")
        uploaded_files = st.file_uploader(
            "Upload documents or images to ground your prompts",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt', 'md', 'png', 'jpg', 'jpeg']
        )
        
        # Tool selection
        st.markdown("##### 🛠️ Select Existing Tools (Optional)")
        available_tools = [
            "Web Search", "Data Analysis", "Code Execution",
            "Document Processing", "API Integration", "Database Query"
        ]
        selected_tools = st.multiselect(
            "Choose tools to include",
            available_tools
        )
        
        submit_button = st.form_submit_button("🎨 Generate & Open in Canvas", use_container_width=True)
        
        if submit_button:
            if not project_name:
                st.error("Please provide a project name")
                return
            
            if not project_description:
                st.error("Please provide a project description")
                return
            
            # Create project
            with st.spinner("🤖 Generating your agent canvas..."):
                project = create_project(
                    project_name,
                    project_description,
                    agent_type,
                    complexity,
                    uploaded_files,
                    selected_tools
                )
                
                st.session_state.project = project
                st.session_state.current_page = 'canvas'
                st.success("✅ Project created! Redirecting to canvas...")
                st.rerun()

def create_project(name: str, description: str, agent_type: str, 
                   complexity: str, files: Any, tools: list) -> Dict[str, Any]:
    """Create a new project from prompt"""
    
    generator = ProjectGenerator()
    
    # Process uploaded files
    documents = []
    if files:
        for file in files:
            documents.append({
                'name': file.name,
                'type': file.type,
                'content': file.read()
            })
    
    # Generate project structure
    project = generator.generate_from_prompt(
        name=name,
        description=description,
        agent_type=agent_type,
        complexity=complexity,
        documents=documents,
        tools=tools
    )
    
    return project

def show_load_project():
    """Display load existing project interface"""
    
    st.markdown("#### Load Existing Project")
    
    # In production, fetch from database
    # For demo, use session state
    if 'user_projects' not in st.session_state:
        st.session_state.user_projects = []
    
    if not st.session_state.user_projects:
        st.info("No saved projects found. Create a new project to get started!")
        return
    
    for project in st.session_state.user_projects:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{project['name']}**")
                st.caption(f"Last modified: {project.get('last_modified', 'Unknown')}")
                st.caption(f"Agents: {len(project.get('agents', []))}")
            
            with col2:
                if st.button("Open", key=f"open_{project['id']}"):
                    st.session_state.project = project
                    st.session_state.current_page = 'canvas'
                    st.rerun()
            
            with col3:
                if st.button("Delete", key=f"delete_{project['id']}"):
                    st.session_state.user_projects.remove(project)
                    st.rerun()
            
            st.markdown("---")

def show_templates():
    """Display available templates"""
    
    st.markdown("#### Start from a Template")
    st.markdown("Choose from pre-built playbooks and scenes")
    
    templates = [
        {
            'name': 'Customer Support Team',
            'description': 'Multi-agent system with triage, support, and escalation agents',
            'agents': 3,
            'icon': '🎧'
        },
        {
            'name': 'Research Assistant',
            'description': 'Single agent for research, summarization, and reporting',
            'agents': 1,
            'icon': '🔍'
        },
        {
            'name': 'Code Review Pipeline',
            'description': 'Automated code analysis, testing, and review agents',
            'agents': 4,
            'icon': '💻'
        },
        {
            'name': 'Data Analysis Workflow',
            'description': 'Extract, analyze, visualize, and report on data',
            'agents': 3,
            'icon': '📊'
        }
    ]
    
    cols = st.columns(2)
    
    for idx, template in enumerate(templates):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"### {template['icon']} {template['name']}")
                st.markdown(template['description'])
                st.caption(f"Agents: {template['agents']}")
                
                if st.button(f"Use Template", key=f"template_{idx}", use_container_width=True):
                    # Load template
                    project = load_template(template)
                    st.session_state.project = project
                    st.session_state.current_page = 'canvas'
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)

def load_template(template: Dict[str, Any]) -> Dict[str, Any]:
    """Load a project template"""
    
    # In production, load from template library
    project = {
        'id': f"template_{datetime.now().timestamp()}",
        'name': template['name'],
        'description': template['description'],
        'agents': [],
        'connections': [],
        'created_at': datetime.now().isoformat(),
        'last_modified': datetime.now().isoformat()
    }
    
    return project

def show_stats_panel():
    """Display user statistics"""
    
    # Mock stats - in production, fetch from database
    stats = {
        'projects': len(st.session_state.get('user_projects', [])),
        'agents': sum(len(p.get('agents', [])) for p in st.session_state.get('user_projects', [])),
        'deployments': 0
    }
    
    st.metric("Projects", stats['projects'])
    st.metric("Agents Created", stats['agents'])
    st.metric("Active Deployments", stats['deployments'])

def show_quick_links():
    """Display quick links"""
    
    st.markdown("[📖 Documentation](https://docs.microsoft.com)")
    st.markdown("[💡 Examples](https://github.com)")
    st.markdown("[❓ Help & Support](https://support.microsoft.com)")
    st.markdown("[🎥 Video Tutorials](https://youtube.com)")
