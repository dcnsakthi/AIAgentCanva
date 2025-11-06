"""
Main Streamlit application for MAF Agent Builder Canvas
"""
import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.pages import landing, canvas, sandbox, evaluation, deployment
from src.auth.auth_manager import AuthManager
from src.utils.config_loader import ConfigLoader

# Page configuration
st.set_page_config(
    page_title="MAF Agent Builder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration
config = ConfigLoader.load_config()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'project' not in st.session_state:
    st.session_state.project = None

def main():
    """Main application entry point"""
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0078D4;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #605E5C;
            margin-bottom: 2rem;
        }
        .stButton>button {
            background-color: #0078D4;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #106EBE;
        }
        .node-card {
            border: 2px solid #E1DFDD;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            background-color: #FFFFFF;
        }
        .sidebar-content {
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Authentication check
    if not st.session_state.authenticated:
        auth_manager = AuthManager()
        auth_manager.show_login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🤖 MAF Agent Builder")
        st.markdown("---")
        
        if st.session_state.user_info:
            st.markdown(f"**User:** {st.session_state.user_info.get('name', 'User')}")
            st.markdown(f"**Email:** {st.session_state.user_info.get('email', '')}")
            st.markdown("---")
        
        # Navigation
        pages = {
            "🏠 Home": "landing",
            "🎨 Canvas Studio": "canvas",
            "🧪 Live Sandbox": "sandbox",
            "✅ Evaluation": "evaluation",
            "🚀 Deployment": "deployment"
        }
        
        for label, page_id in pages.items():
            if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.markdown("---")
        
        # Project info
        if st.session_state.project:
            st.markdown("### 📁 Current Project")
            st.markdown(f"**Name:** {st.session_state.project.get('name', 'Untitled')}")
            st.markdown(f"**Agents:** {len(st.session_state.project.get('agents', []))}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.project = None
            st.rerun()
    
    # Main content area
    page = st.session_state.current_page
    
    if page == 'landing':
        landing.show()
    elif page == 'canvas':
        canvas.show()
    elif page == 'sandbox':
        sandbox.show()
    elif page == 'evaluation':
        evaluation.show()
    elif page == 'deployment':
        deployment.show()
    else:
        st.error("Page not found")

if __name__ == "__main__":
    main()
