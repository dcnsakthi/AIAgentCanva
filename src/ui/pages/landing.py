"""
Landing page - Prompt-to-canvas flow
"""
import streamlit as st
from typing import Dict, Any
import json
from datetime import datetime
from src.utils.config_loader import ConfigLoader
from src.agents.project_generator import ProjectGenerator
from src.ui.templates import AgentTemplate

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
    """Display available templates with enhanced filtering"""
    
    st.markdown("#### 📚 Start from a Template")
    st.markdown("Choose from pre-built playbooks and scenes")
    
    # Info section
    with st.expander("ℹ️ About Templates", expanded=False):
        st.markdown("""
        **Templates** are pre-configured agent systems designed for common business scenarios. Each template includes:
        
        - 🤖 **Pre-configured agents** with specialized roles and system prompts
        - 🔗 **Agent connections** defining workflow patterns
        - 🛠️ **Recommended tools** for the specific use case
        - 📋 **Use case examples** to guide implementation
        
        **Quick Tips:**
        - Start with a template close to your needs
        - Customize agents and prompts after loading
        - Use the canvas to modify workflows visually
        - Test templates with evaluation tools before deployment
        """)
    
    # Get all templates
    all_templates = AgentTemplate.get_all_templates()
    
    # Filter controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search templates", placeholder="Search by name, description, or tags...")
    
    with col2:
        categories = ['All'] + sorted(list(set([t['category'] for t in all_templates])))
        selected_category = st.selectbox("Category", categories)
    
    with col3:
        complexities = ['All', 'Simple', 'Moderate', 'Complex', 'Enterprise']
        selected_complexity = st.selectbox("Complexity", complexities)
    
    # Filter templates
    filtered_templates = all_templates
    
    if search_query:
        filtered_templates = AgentTemplate.search_templates(search_query)
    
    if selected_category != 'All':
        filtered_templates = [t for t in filtered_templates if t['category'] == selected_category]
    
    if selected_complexity != 'All':
        filtered_templates = [t for t in filtered_templates if t['complexity'] == selected_complexity]
    
    # Display count
    st.markdown(f"*Found {len(filtered_templates)} template(s)*")
    st.markdown("---")
    
    # Display templates in a grid
    if not filtered_templates:
        st.info("No templates found matching your criteria.")
        return
    
    # Create 2-column layout for templates
    for idx in range(0, len(filtered_templates), 2):
        cols = st.columns(2)
        
        for col_idx, col in enumerate(cols):
            if idx + col_idx < len(filtered_templates):
                template = filtered_templates[idx + col_idx]
                
                with col:
                    with st.container():
                        # Template card
                        st.markdown(f"### {template['icon']} {template['name']}")
                        st.markdown(f"**{template['category']}** • {template['complexity']}")
                        st.markdown(template['description'])
                        
                        # Details in expander
                        with st.expander("View Details"):
                            st.markdown(f"**Agents:** {template['agents_count']}")
                            st.markdown(f"**Setup Time:** {template['estimated_setup_time']}")
                            
                            st.markdown("**Use Cases:**")
                            for use_case in template['use_cases']:
                                st.markdown(f"- {use_case}")
                            
                            st.markdown("**Included Tools:**")
                            for tool in template['tools']:
                                st.markdown(f"- {tool}")
                            
                            st.markdown("**Tags:**")
                            st.markdown(", ".join([f"`{tag}`" for tag in template['tags']]))
                        
                        # Use template button
                        if st.button(
                            "Use This Template",
                            key=f"template_{template['id']}",
                            use_container_width=True,
                            type="primary"
                        ):
                            project = AgentTemplate.load_template_as_project(template)
                            st.session_state.project = project
                            st.session_state.current_page = 'canvas'
                            st.success(f"✅ Loaded template: {template['name']}")
                            st.rerun()
                        
                        st.markdown("<br>", unsafe_allow_html=True)

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
