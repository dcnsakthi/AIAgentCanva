"""
Canvas Studio - Visual drag-and-drop builder
"""
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import json
from typing import Dict, Any, List
from src.utils.config_loader import ConfigLoader
from src.agents.agent_types import AgentFactory

def show():
    """Display canvas studio page"""
    
    if not st.session_state.project:
        st.warning("No project loaded. Please create or load a project from the home page.")
        if st.button("Go to Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
        return
    
    st.markdown(f"<h1 class='main-header'>🎨 Canvas Studio</h1>", unsafe_allow_html=True)
    st.markdown(f"**Project:** {st.session_state.project.get('name', 'Untitled')}")
    
    # Show template guide if loaded from template
    if st.session_state.get('template_loaded') and st.session_state.get('show_template_guide'):
        show_template_guide()
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        show_canvas()
    
    with col2:
        show_properties_panel()

def show_template_guide():
    """Show helpful guide when template is loaded"""
    
    project = st.session_state.project
    template_meta = project.get('template_metadata', {})
    
    with st.container():
        st.info(f"""
        **✅ Template Loaded: {template_meta.get('template_name', 'Unknown')}**
        
        **What's Ready:**
        - ✅ {len(project.get('agents', []))} agents configured with roles and prompts
        - ✅ {len(project.get('connections', []))} connections defining the workflow
        - ✅ Auto-layout applied for clear visualization
        - ✅ Ready to test in sandbox
        
        **Next Steps:**
        1. **Review**: Check agents and connections below
        2. **Customize**: Click any agent to edit prompts and settings
        3. **Test**: Go to Sandbox to test with sample queries
        4. **Save**: Use the Save button to preserve changes
        
        **Quick Actions:**
        """)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🧪 Test in Sandbox", use_container_width=True, type="primary"):
                st.session_state.current_page = 'sandbox'
                st.session_state.show_template_guide = False
                st.rerun()
        
        with col2:
            if st.button("📋 View Use Cases", use_container_width=True):
                st.session_state.show_use_cases = True
                st.rerun()
        
        with col3:
            if st.button("💾 Save Project", use_container_width=True):
                save_project()
                st.success("Project saved!")
        
        with col4:
            if st.button("❌ Dismiss", use_container_width=True):
                st.session_state.show_template_guide = False
                st.rerun()
    
    # Show use cases if requested
    if st.session_state.get('show_use_cases'):
        with st.expander("📋 Template Use Cases", expanded=True):
            use_cases = template_meta.get('use_cases', [])
            if use_cases:
                for i, use_case in enumerate(use_cases, 1):
                    st.markdown(f"{i}. {use_case}")
            else:
                st.info("No specific use cases documented for this template.")
            
            if st.button("Close Use Cases"):
                st.session_state.show_use_cases = False
                st.rerun()
    
    st.markdown("---")

def show_canvas():
    """Display the main canvas with drag-and-drop functionality"""
    
    st.markdown("### Agent Canvas")
    
    # Initialize canvas data from project if not already set
    if 'canvas_nodes' not in st.session_state or st.session_state.get('template_loaded'):
        # Load from project
        st.session_state.canvas_nodes = st.session_state.project.get('agents', [])
        if st.session_state.get('template_loaded'):
            st.session_state.template_loaded = False  # Reset flag after loading
    
    if 'canvas_edges' not in st.session_state:
        st.session_state.canvas_edges = st.session_state.project.get('connections', [])
    
    if 'selected_node' not in st.session_state:
        st.session_state.selected_node = None
    if 'show_agent_selector' not in st.session_state:
        st.session_state.show_agent_selector = False
    if 'connection_mode' not in st.session_state:
        st.session_state.connection_mode = False
    
    # Toolbar
    show_toolbar()
    
    # Show agent selector if button was clicked
    if st.session_state.show_agent_selector:
        show_agent_selector()
    
    # Show connection dialog if in connection mode
    if st.session_state.connection_mode:
        show_connection_dialog()
    
    # Canvas area
    canvas_container = st.container()
    
    with canvas_container:
        # Render graph
        render_agent_graph()

def show_toolbar():
    """Display canvas toolbar"""
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("➕ Add Agent"):
            st.session_state.show_agent_selector = not st.session_state.get('show_agent_selector', False)
            st.rerun()
    
    with col2:
        button_type = "primary" if st.session_state.get('connection_mode') else "secondary"
        if st.button("🔗 Connect", type=button_type):
            st.session_state.connection_mode = not st.session_state.get('connection_mode', False)
            st.rerun()
    
    with col3:
        if st.button("💾 Save"):
            save_project()
            st.success("Project saved!")
    
    with col4:
        if st.button("🔄 Auto-Layout"):
            auto_layout_canvas()
            st.success("✅ Layout applied!")
            st.rerun()
    
    with col5:
        if st.button("🧹 Clear"):
            if st.session_state.get('confirm_clear'):
                clear_canvas()
                st.session_state.confirm_clear = False
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm")
    
    with col6:
        if st.button("📤 Export"):
            export_project()

def show_agent_selector():
    """Show agent type selector dialog"""
    
    config = ConfigLoader.load_config()
    agent_types = config.get('agent_types', [])
    
    st.markdown("---")
    st.markdown("### 🎯 Select Agent Type")
    
    # Close button
    if st.button("❌ Close", key="close_selector"):
        st.session_state.show_agent_selector = False
        st.rerun()
    
    st.markdown("---")
    
    for agent_type in agent_types:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"<h2>{agent_type['icon']}</h2>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{agent_type['name']}**")
                st.caption(agent_type['description'])
                
                if st.button(f"Add {agent_type['name']}", key=f"add_{agent_type['id']}"):
                    add_agent_to_canvas(agent_type)
                    st.session_state.show_agent_selector = False
                    st.rerun()
            
            st.markdown("---")

def add_agent_to_canvas(agent_type: Dict[str, Any]):
    """Add a new agent to the canvas"""
    
    # Generate unique ID
    agent_id = f"agent_{len(st.session_state.canvas_nodes)}"
    
    # Create agent node
    node = {
        'id': agent_id,
        'type': agent_type['id'],
        'name': f"{agent_type['name']} {len(st.session_state.canvas_nodes) + 1}",
        'icon': agent_type['icon'],
        'system_prompt': agent_type['default_system_prompt'],
        'llm_model': 'gpt-4',
        'temperature': 0.7,
        'max_tokens': 1000,
        'tools': [],
        'vector_db': None,
        'position': {
            'x': 100 + (len(st.session_state.canvas_nodes) * 50),
            'y': 100 + (len(st.session_state.canvas_nodes) * 50)
        }
    }
    
    st.session_state.canvas_nodes.append(node)
    st.session_state.project['agents'] = st.session_state.canvas_nodes

def show_connection_dialog():
    """Show dialog to connect agents"""
    
    st.markdown("---")
    st.markdown("### 🔗 Connect Agents")
    
    if len(st.session_state.canvas_nodes) < 2:
        st.warning("⚠️ You need at least 2 agents to create a connection")
        if st.button("Close", key="close_connect_warning"):
            st.session_state.connection_mode = False
            st.rerun()
        return
    
    # Close button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("❌ Close", key="close_connector"):
            st.session_state.connection_mode = False
            st.rerun()
    
    st.markdown("---")
    
    # Get agent names for dropdown
    agent_options = {node['name']: node['id'] for node in st.session_state.canvas_nodes}
    agent_names = list(agent_options.keys())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**From Agent:**")
        source_name = st.selectbox(
            "Source",
            agent_names,
            key="connect_source",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**To Agent:**")
        target_name = st.selectbox(
            "Target",
            agent_names,
            key="connect_target",
            label_visibility="collapsed"
        )
    
    # Connection label
    connection_label = st.text_input(
        "Connection Label (optional)",
        placeholder="e.g., 'sends data to', 'reviews output from'",
        key="connection_label"
    )
    
    st.markdown("---")
    
    if st.button("➕ Create Connection", type="primary", use_container_width=True):
        source_id = agent_options[source_name]
        target_id = agent_options[target_name]
        
        if source_id == target_id:
            st.error("❌ Cannot connect an agent to itself")
        else:
            # Check if connection already exists
            existing = any(
                e['source'] == source_id and e['target'] == target_id 
                for e in st.session_state.canvas_edges
            )
            
            if existing:
                st.warning("⚠️ This connection already exists")
            else:
                # Add edge
                edge = {
                    'source': source_id,
                    'target': target_id,
                    'label': connection_label if connection_label else None
                }
                st.session_state.canvas_edges.append(edge)
                st.success(f"✅ Connected {source_name} → {target_name}")
                st.session_state.connection_mode = False
                st.rerun()
    
    # Show existing connections
    if st.session_state.canvas_edges:
        st.markdown("---")
        st.markdown("**Existing Connections:**")
        
        for i, edge in enumerate(st.session_state.canvas_edges):
            source_node = next((n for n in st.session_state.canvas_nodes if n['id'] == edge['source']), None)
            target_node = next((n for n in st.session_state.canvas_nodes if n['id'] == edge['target']), None)
            
            if source_node and target_node:
                col1, col2 = st.columns([4, 1])
                with col1:
                    label_text = f" ({edge['label']})" if edge.get('label') else ""
                    st.text(f"{source_node['name']} → {target_node['name']}{label_text}")
                with col2:
                    if st.button("🗑️", key=f"delete_edge_{i}"):
                        st.session_state.canvas_edges.pop(i)
                        st.rerun()

def render_agent_graph():
    """Render the agent graph visualization"""
    
    nodes = []
    edges = []
    
    # Convert nodes
    for node in st.session_state.canvas_nodes:
        nodes.append(Node(
            id=node['id'],
            label=node['name'],
            size=30,
            shape="box",
            color="#0078D4"
        ))
    
    # Convert edges
    for edge in st.session_state.canvas_edges:
        edges.append(Edge(
            source=edge['source'],
            target=edge['target'],
            type="CURVE_SMOOTH"
        ))
    
    # Graph configuration
    config = Config(
        width=800,
        height=600,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=True,
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': True}
    )
    
    if nodes:
        return_value = agraph(nodes=nodes, edges=edges, config=config)
        
        if return_value:
            st.session_state.selected_node = return_value
    else:
        st.info("👆 Click 'Add Agent' to start building your agent system")

def show_properties_panel():
    """Display properties panel for selected agent"""
    
    st.markdown("### Properties")
    
    if st.session_state.selected_node:
        # Find selected node
        node = next(
            (n for n in st.session_state.canvas_nodes if n['id'] == st.session_state.selected_node),
            None
        )
        
        if node:
            show_agent_properties(node)
    else:
        st.info("Select an agent to edit its properties")

def show_agent_properties(node: Dict[str, Any]):
    """Display and edit agent properties"""
    
    st.markdown(f"#### {node['icon']} {node['name']}")
    
    with st.form(key=f"props_{node['id']}"):
        # Basic properties
        node['name'] = st.text_input("Name", value=node['name'])
        
        # LLM Configuration
        st.markdown("##### 🤖 LLM Configuration")
        
        config = ConfigLoader.load_config()
        available_models = []
        
        for provider in config.get('llm_providers', {}).values():
            if provider.get('enabled'):
                for model in provider.get('models', []):
                    available_models.append(model['display_name'])
        
        node['llm_model'] = st.selectbox(
            "Model",
            available_models,
            index=available_models.index(node.get('llm_model', available_models[0])) if node.get('llm_model') in available_models else 0
        )
        
        node['temperature'] = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=node.get('temperature', 0.7),
            step=0.1
        )
        
        node['max_tokens'] = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=32000,
            value=node.get('max_tokens', 1000),
            step=100
        )
        
        # System Prompt
        st.markdown("##### 💬 System Prompt")
        node['system_prompt'] = st.text_area(
            "System Prompt",
            value=node.get('system_prompt', ''),
            height=150
        )
        
        # Tools
        st.markdown("##### 🛠️ Tools")
        available_tools = ["Web Search", "Code Execution", "Data Analysis", "Document Processing"]
        node['tools'] = st.multiselect(
            "Select Tools",
            available_tools,
            default=node.get('tools', [])
        )
        
        # Vector Database
        st.markdown("##### 📚 Knowledge Base")
        vector_dbs = ["None", "ChromaDB", "FAISS", "Pinecone", "Qdrant"]
        node['vector_db'] = st.selectbox(
            "Vector Database",
            vector_dbs,
            index=vector_dbs.index(node.get('vector_db', 'None')) if node.get('vector_db') in vector_dbs else 0
        )
        
        # Submit button
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Save Changes", use_container_width=True):
                st.success("Changes saved!")
                st.rerun()
        
        with col2:
            if st.form_submit_button("Delete Agent", use_container_width=True):
                st.session_state.canvas_nodes = [
                    n for n in st.session_state.canvas_nodes if n['id'] != node['id']
                ]
                st.session_state.selected_node = None
                st.rerun()

def save_project():
    """Save current project"""
    st.session_state.project['agents'] = st.session_state.canvas_nodes
    st.session_state.project['connections'] = st.session_state.canvas_edges
    
    # In production, save to database
    if 'user_projects' not in st.session_state:
        st.session_state.user_projects = []
    
    # Update or add project
    existing = next(
        (p for p in st.session_state.user_projects if p['id'] == st.session_state.project['id']),
        None
    )
    
    if existing:
        existing.update(st.session_state.project)
    else:
        st.session_state.user_projects.append(st.session_state.project)

def auto_layout_canvas():
    """Automatically layout agents on canvas"""
    
    num_nodes = len(st.session_state.canvas_nodes)
    
    if num_nodes == 0:
        return
    
    # Check if there are connections to determine layout type
    has_connections = len(st.session_state.canvas_edges) > 0
    
    if has_connections:
        # Hierarchical layout for connected agents
        layout_hierarchical()
    else:
        # Grid layout for unconnected agents
        layout_grid()

def layout_grid():
    """Simple grid layout"""
    num_nodes = len(st.session_state.canvas_nodes)
    
    # Calculate optimal grid size
    import math
    grid_cols = math.ceil(math.sqrt(num_nodes))
    grid_rows = math.ceil(num_nodes / grid_cols)
    
    spacing_x = 250
    spacing_y = 200
    
    # Calculate total dimensions
    total_width = (grid_cols - 1) * spacing_x
    total_height = (grid_rows - 1) * spacing_y
    
    # Center the layout (canvas width ~800px, height ~600px)
    start_x = (800 - total_width) / 2
    start_y = (600 - total_height) / 2
    
    # Ensure minimum margins
    start_x = max(100, start_x)
    start_y = max(100, start_y)
    
    for idx, node in enumerate(st.session_state.canvas_nodes):
        row = idx // grid_cols
        col = idx % grid_cols
        node['position'] = {
            'x': start_x + (col * spacing_x),
            'y': start_y + (row * spacing_y)
        }

def layout_hierarchical():
    """Hierarchical layout based on connections"""
    
    # Build adjacency list
    graph = {node['id']: [] for node in st.session_state.canvas_nodes}
    in_degree = {node['id']: 0 for node in st.session_state.canvas_nodes}
    
    for edge in st.session_state.canvas_edges:
        graph[edge['source']].append(edge['target'])
        in_degree[edge['target']] += 1
    
    # Find root nodes (no incoming edges)
    roots = [node_id for node_id, degree in in_degree.items() if degree == 0]
    
    # If no roots (circular), pick the first node
    if not roots:
        roots = [st.session_state.canvas_nodes[0]['id']]
    
    # BFS to assign levels
    levels = {}
    queue = [(root, 0) for root in roots]
    visited = set()
    
    while queue:
        node_id, level = queue.pop(0)
        if node_id in visited:
            continue
        visited.add(node_id)
        levels[node_id] = level
        
        for neighbor in graph[node_id]:
            if neighbor not in visited:
                queue.append((neighbor, level + 1))
    
    # Assign unvisited nodes to level 0
    for node in st.session_state.canvas_nodes:
        if node['id'] not in levels:
            levels[node['id']] = 0
    
    # Group nodes by level
    level_groups = {}
    for node_id, level in levels.items():
        if level not in level_groups:
            level_groups[level] = []
        level_groups[level].append(node_id)
    
    # Calculate layout dimensions
    spacing_x = 250
    spacing_y = 180
    max_nodes_at_level = max(len(node_ids) for node_ids in level_groups.values())
    num_levels = len(level_groups)
    
    # Calculate total dimensions
    total_width = (max_nodes_at_level - 1) * spacing_x
    total_height = (num_levels - 1) * spacing_y
    
    # Center the layout (canvas width ~800px, height ~600px)
    canvas_center_x = 400
    canvas_center_y = 300
    
    start_y = canvas_center_y - (total_height / 2)
    start_y = max(80, start_y)  # Minimum top margin
    
    # Layout nodes
    for level, node_ids in level_groups.items():
        # Center nodes horizontally at each level
        num_at_level = len(node_ids)
        level_width = (num_at_level - 1) * spacing_x
        level_start_x = canvas_center_x - (level_width / 2)
        
        for idx, node_id in enumerate(node_ids):
            node = next((n for n in st.session_state.canvas_nodes if n['id'] == node_id), None)
            if node:
                node['position'] = {
                    'x': level_start_x + (idx * spacing_x),
                    'y': start_y + (level * spacing_y)
                }

def clear_canvas():
    """Clear all agents from canvas"""
    st.session_state.canvas_nodes = []
    st.session_state.canvas_edges = []
    st.session_state.selected_node = None

def export_project():
    """Export project to JSON"""
    project_json = json.dumps(st.session_state.project, indent=2)
    st.download_button(
        label="Download Project JSON",
        data=project_json,
        file_name=f"{st.session_state.project['name']}.json",
        mime="application/json"
    )
