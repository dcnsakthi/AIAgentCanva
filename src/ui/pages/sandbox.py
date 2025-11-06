"""
Live Preview Sandbox - Test agents in browser
"""
import streamlit as st
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from src.agents.agent_executor import AgentExecutor

def show():
    """Display sandbox page"""
    
    if not st.session_state.project:
        st.warning("No project loaded. Please create or load a project from the home page.")
        if st.button("Go to Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
        return
    
    st.markdown("<h1 class='main-header'>🧪 Live Preview Sandbox</h1>", unsafe_allow_html=True)
    st.markdown("Test your agents in a safe sandbox environment")
    
    # Initialize sandbox state
    if 'sandbox_messages' not in st.session_state:
        st.session_state.sandbox_messages = []
    if 'sandbox_executor' not in st.session_state:
        st.session_state.sandbox_executor = AgentExecutor(st.session_state.project)
    
    # Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_chat_interface()
    
    with col2:
        show_execution_panel()

def show_chat_interface():
    """Display chat interface for testing agents"""
    
    st.markdown("### 💬 Test Conversation")
    
    # Agent selector
    agents = st.session_state.project.get('agents', [])
    
    if not agents:
        st.warning("No agents in project. Add agents in the Canvas Studio.")
        return
    
    agent_names = [agent['name'] for agent in agents]
    selected_agent = st.selectbox(
        "Select Agent to Test",
        agent_names
    )
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.sandbox_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                if "metadata" in message:
                    with st.expander("View Details"):
                        st.json(message["metadata"])
    
    # Input area
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Add user message
        st.session_state.sandbox_messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get agent response
        with st.spinner("Agent thinking..."):
            agent = next(a for a in agents if a['name'] == selected_agent)
            response = execute_agent(agent, user_input)
            
            # Add assistant message
            st.session_state.sandbox_messages.append({
                "role": "assistant",
                "content": response['content'],
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "agent": agent['name'],
                    "model": agent['llm_model'],
                    "tokens": response.get('tokens', 0),
                    "duration": response.get('duration', 0)
                }
            })
        
        st.rerun()
    
    # Clear button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.sandbox_messages = []
        st.rerun()

def execute_agent(agent: Dict[str, Any], user_input: str) -> Dict[str, Any]:
    """Execute agent with user input"""
    
    executor = st.session_state.sandbox_executor
    
    try:
        start_time = datetime.now()
        
        # Execute agent
        result = executor.run_agent(agent['id'], user_input)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return {
            'content': result.get('response', 'No response'),
            'tokens': result.get('tokens_used', 0),
            'duration': duration,
            'success': True
        }
    
    except Exception as e:
        return {
            'content': f"Error: {str(e)}",
            'tokens': 0,
            'duration': 0,
            'success': False
        }

def show_execution_panel():
    """Display execution metrics and controls"""
    
    st.markdown("### 📊 Execution Metrics")
    
    # Calculate metrics
    total_messages = len(st.session_state.sandbox_messages)
    user_messages = len([m for m in st.session_state.sandbox_messages if m['role'] == 'user'])
    assistant_messages = len([m for m in st.session_state.sandbox_messages if m['role'] == 'assistant'])
    
    total_tokens = sum(
        m.get('metadata', {}).get('tokens', 0) 
        for m in st.session_state.sandbox_messages 
        if 'metadata' in m
    )
    
    avg_duration = 0
    if assistant_messages > 0:
        total_duration = sum(
            m.get('metadata', {}).get('duration', 0) 
            for m in st.session_state.sandbox_messages 
            if 'metadata' in m
        )
        avg_duration = total_duration / assistant_messages
    
    # Display metrics
    st.metric("Total Messages", total_messages)
    st.metric("User Messages", user_messages)
    st.metric("Agent Responses", assistant_messages)
    st.metric("Total Tokens", f"{total_tokens:,}")
    st.metric("Avg Response Time", f"{avg_duration:.2f}s")
    
    st.markdown("---")
    
    # Sandbox controls
    st.markdown("### ⚙️ Sandbox Controls")
    
    if st.button("🔄 Reset Sandbox", use_container_width=True):
        st.session_state.sandbox_messages = []
        st.session_state.sandbox_executor = AgentExecutor(st.session_state.project)
        st.rerun()
    
    if st.button("📥 Export Conversation", use_container_width=True):
        export_conversation()
    
    # Debug mode
    debug_mode = st.checkbox("Enable Debug Mode")
    
    if debug_mode:
        st.markdown("### 🐛 Debug Info")
        with st.expander("View Session State"):
            st.json({
                'messages_count': len(st.session_state.sandbox_messages),
                'project_id': st.session_state.project.get('id'),
                'agents_count': len(st.session_state.project.get('agents', []))
            })

def export_conversation():
    """Export conversation to file"""
    import json
    
    conversation_data = {
        'project_name': st.session_state.project.get('name'),
        'timestamp': datetime.now().isoformat(),
        'messages': st.session_state.sandbox_messages
    }
    
    json_data = json.dumps(conversation_data, indent=2)
    
    st.download_button(
        label="Download Conversation",
        data=json_data,
        file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
