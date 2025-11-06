"""
Authentication manager for multiple authentication providers
"""
import streamlit as st
from typing import Optional, Dict, Any
import jwt
import time
from datetime import datetime, timedelta
import hashlib
import secrets
from msal import ConfidentialClientApplication
import requests
from src.utils.config_loader import ConfigLoader

class AuthManager:
    """Manages authentication across multiple providers"""
    
    def __init__(self):
        self.config = ConfigLoader.load_config()
        self.jwt_secret = ConfigLoader.get_env("JWT_SECRET_KEY", "default-secret-key")
        
    def show_login_page(self):
        """Display login page with multiple authentication options"""
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<h1 class='main-header' style='text-align: center;'>🤖 MAF Agent Builder</h1>", 
                       unsafe_allow_html=True)
            st.markdown("<p class='sub-header' style='text-align: center;'>Build powerful AI agents with Microsoft Agent Framework</p>",
                       unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Authentication tabs
            auth_tab = st.tabs(["🔐 Sign In", "📝 Quick Start (Demo)"])
            
            with auth_tab[0]:
                st.markdown("### Choose your authentication method")
                
                # GitHub OAuth
                if st.button("🐙 Sign in with GitHub", use_container_width=True):
                    self._github_login()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Microsoft Entra ID (Azure AD)
                if st.button("🔷 Sign in with Microsoft", use_container_width=True):
                    self._microsoft_login()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Email Magic Link
                st.markdown("### Or use email magic link")
                email = st.text_input("Enter your email", key="magic_link_email")
                if st.button("📧 Send Magic Link", use_container_width=True):
                    if email:
                        self._send_magic_link(email)
                        st.success(f"Magic link sent to {email}! Check your inbox.")
                    else:
                        st.error("Please enter a valid email address")
            
            with auth_tab[1]:
                st.markdown("### Quick Start - Demo Mode")
                st.info("Skip authentication and try the builder with demo credentials. Perfect for testing!")
                
                demo_name = st.text_input("Your Name", value="Demo User", key="demo_name")
                
                if st.button("🚀 Start Demo", use_container_width=True):
                    self._demo_login(demo_name)
                    st.rerun()
    
    def _github_login(self):
        """Handle GitHub OAuth login"""
        client_id = ConfigLoader.get_env("GITHUB_CLIENT_ID")
        
        if not client_id:
            st.error("GitHub authentication not configured. Please set GITHUB_CLIENT_ID in .env")
            return
        
        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        st.session_state.oauth_state = state
        
        # GitHub OAuth URL
        redirect_uri = ConfigLoader.get_env("GITHUB_REDIRECT_URI", "http://localhost:8501")
        oauth_url = (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"state={state}&"
            f"scope=user:email"
        )
        
        st.markdown(f"[Click here to authorize with GitHub]({oauth_url})")
        st.info("After authorization, you'll be redirected back to the application.")
    
    def _microsoft_login(self):
        """Handle Microsoft Entra ID (Azure AD) login"""
        client_id = ConfigLoader.get_env("MICROSOFT_CLIENT_ID")
        client_secret = ConfigLoader.get_env("MICROSOFT_CLIENT_SECRET")
        tenant_id = ConfigLoader.get_env("MICROSOFT_TENANT_ID")
        
        if not all([client_id, client_secret, tenant_id]):
            st.error("Microsoft authentication not configured. Please set credentials in .env")
            return
        
        try:
            # Create MSAL app
            authority = f"https://login.microsoftonline.com/{tenant_id}"
            app = ConfidentialClientApplication(
                client_id,
                authority=authority,
                client_credential=client_secret
            )
            
            # Generate auth URL
            redirect_uri = ConfigLoader.get_env("MICROSOFT_REDIRECT_URI", "http://localhost:8501")
            auth_url = app.get_authorization_request_url(
                scopes=["User.Read"],
                redirect_uri=redirect_uri
            )
            
            st.markdown(f"[Click here to sign in with Microsoft]({auth_url})")
            st.info("After authorization, you'll be redirected back to the application.")
            
        except Exception as e:
            st.error(f"Error initiating Microsoft login: {str(e)}")
    
    def _send_magic_link(self, email: str):
        """Send magic link to user's email"""
        # Generate token
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(minutes=15)
        
        # Store token in session (in production, use database)
        if 'magic_tokens' not in st.session_state:
            st.session_state.magic_tokens = {}
        
        st.session_state.magic_tokens[token] = {
            'email': email,
            'expiry': expiry
        }
        
        # In production, send actual email via SendGrid or similar service
        magic_link = f"http://localhost:8501?magic_token={token}"
        
        # For demo purposes, show the link
        st.code(f"Magic link (demo): {magic_link}", language=None)
        st.warning("⚠️ In production, this link would be sent to your email via SendGrid.")
    
    def _demo_login(self, name: str):
        """Handle demo login"""
        st.session_state.authenticated = True
        st.session_state.user_info = {
            'name': name,
            'email': 'demo@example.com',
            'provider': 'demo',
            'user_id': hashlib.md5(name.encode()).hexdigest()
        }
        
        # Create JWT token
        token_data = {
            'user_id': st.session_state.user_info['user_id'],
            'email': st.session_state.user_info['email'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        
        token = jwt.encode(token_data, self.jwt_secret, algorithm='HS256')
        st.session_state.auth_token = token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user_info = None
        if 'auth_token' in st.session_state:
            del st.session_state.auth_token
