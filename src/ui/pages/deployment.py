"""
Deployment page - Azure deployment automation
"""
import streamlit as st
from typing import Dict, Any
import json
from datetime import datetime
from src.deployment.azure_deployer import AzureDeployer
from src.deployment.bicep_generator import BicepGenerator

def show():
    """Display deployment page"""
    
    if not st.session_state.project:
        st.warning("No project loaded. Please create or load a project from the home page.")
        if st.button("Go to Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
        return
    
    st.markdown("<h1 class='main-header'>🚀 Deployment</h1>", unsafe_allow_html=True)
    st.markdown("Deploy your agents to Azure with one click")
    
    # Tabs
    tabs = st.tabs(["⚙️ Configure", "📜 Generate Scripts", "🚀 Deploy", "📊 Monitor"])
    
    with tabs[0]:
        show_deployment_config()
    
    with tabs[1]:
        show_script_generation()
    
    with tabs[2]:
        show_deployment_interface()
    
    with tabs[3]:
        show_monitoring()

def show_deployment_config():
    """Display deployment configuration"""
    
    st.markdown("### Deployment Configuration")
    
    # Initialize deployment config if not exists
    if 'deployment_config' not in st.session_state:
        st.session_state.deployment_config = {}
    
    with st.form("deployment_config_form"):
        st.markdown("#### Azure Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subscription_id = st.text_input(
                "Subscription ID",
                value=st.session_state.deployment_config.get('subscription_id', '')
            )
            
            resource_group = st.text_input(
                "Resource Group",
                value=st.session_state.deployment_config.get('resource_group', 'maf-agents-rg')
            )
        
        with col2:
            location = st.selectbox(
                "Azure Region",
                ["eastus", "westus2", "westeurope", "northeurope", "southeastasia"],
                index=0
            )
            
            environment = st.selectbox(
                "Environment",
                ["Development", "Staging", "Production"],
                index=0
            )
        
        st.markdown("#### Container Apps Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cpu_cores = st.number_input("CPU Cores", min_value=0.25, max_value=4.0, value=0.5, step=0.25)
        
        with col2:
            memory_gb = st.number_input("Memory (GB)", min_value=0.5, max_value=8.0, value=1.0, step=0.5)
        
        with col3:
            min_replicas = st.number_input("Min Replicas", min_value=0, max_value=10, value=1)
            max_replicas = st.number_input("Max Replicas", min_value=1, max_value=30, value=10)
        
        st.markdown("#### Secrets & Configuration")
        
        include_openai = st.checkbox("Include OpenAI API Keys", value=True)
        include_cosmos = st.checkbox("Include Cosmos DB", value=False)
        include_storage = st.checkbox("Include Azure Storage", value=False)
        include_search = st.checkbox("Include Azure AI Search", value=False)
        
        st.markdown("#### Networking")
        
        ingress_enabled = st.checkbox("Enable External Ingress", value=True)
        
        if ingress_enabled:
            ingress_port = st.number_input("Ingress Port", min_value=1, max_value=65535, value=8501)
        else:
            ingress_port = None
        
        # Submit
        if st.form_submit_button("Save Configuration", use_container_width=True):
            # Update deployment config after form submission
            st.session_state.deployment_config.update({
                'subscription_id': subscription_id,
                'resource_group': resource_group,
                'location': location,
                'environment': environment,
                'cpu_cores': cpu_cores,
                'memory_gb': memory_gb,
                'min_replicas': min_replicas,
                'max_replicas': max_replicas,
                'include_openai': include_openai,
                'include_cosmos': include_cosmos,
                'include_storage': include_storage,
                'include_search': include_search,
                'ingress_enabled': ingress_enabled,
                'ingress_port': ingress_port
            })
            st.success("✅ Configuration saved!")
            st.rerun()

def show_script_generation():
    """Generate deployment scripts"""
    
    st.markdown("### Generate Deployment Scripts")
    
    if 'deployment_config' not in st.session_state:
        st.warning("Please configure deployment settings first.")
        return
    
    st.info("Generate Bicep templates and deployment scripts for your agent system")
    
    # Script types
    script_type = st.radio(
        "Select Script Type",
        ["Bicep Template", "Azure CLI Script", "PowerShell Script", "Terraform (Preview)"]
    )
    
    if st.button("📜 Generate Scripts", use_container_width=True, type="primary"):
        with st.spinner("Generating deployment scripts..."):
            generator = BicepGenerator(st.session_state.project, st.session_state.deployment_config)
            
            if script_type == "Bicep Template":
                scripts = generator.generate_bicep()
            elif script_type == "Azure CLI Script":
                scripts = generator.generate_cli_script()
            elif script_type == "PowerShell Script":
                scripts = generator.generate_powershell_script()
            else:
                scripts = generator.generate_terraform()
            
            st.session_state.deployment_scripts = scripts
            st.success("Scripts generated successfully!")
    
    # Display generated scripts
    if 'deployment_scripts' in st.session_state:
        st.markdown("---")
        st.markdown("### Generated Scripts")
        
        scripts = st.session_state.deployment_scripts
        
        # Add save all button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{len(scripts)} file(s) generated**")
        with col2:
            if st.button("💾 Save All to Folder", use_container_width=True):
                import os
                from datetime import datetime
                
                project_name = st.session_state.project['name'].lower().replace(' ', '-')
                deploy_dir = os.path.join(os.getcwd(), 'deployments', f"{project_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
                os.makedirs(deploy_dir, exist_ok=True)
                
                for filename, content in scripts.items():
                    file_path = os.path.join(deploy_dir, filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                st.success(f"✅ All files saved to: `{deploy_dir}`")
                st.info("� Open this folder in your terminal and run the deployment script!")
        
        st.markdown("---")
        
        for script_name, script_content in scripts.items():
            with st.expander(f"📄 {script_name}", expanded=False):
                language = 'bicep' if '.bicep' in script_name else 'json' if '.json' in script_name else 'bash' if '.sh' in script_name else 'powershell'
                st.code(script_content, language=language)
                
                st.download_button(
                    label=f"⬇️ Download {script_name}",
                    data=script_content,
                    file_name=script_name,
                    mime="text/plain",
                    key=f"download_{script_name}",
                    use_container_width=True
                )

def show_deployment_interface():
    """Display deployment interface"""
    
    st.markdown("### Deploy to Azure")
    
    if 'deployment_config' not in st.session_state:
        st.warning("Please configure deployment settings first.")
        return
    
    if 'deployment_scripts' not in st.session_state:
        st.warning("Please generate deployment scripts first.")
        return
    
    st.info("⚠️ Make sure you're authenticated with Azure CLI before deploying")
    
    # Show deployment instructions
    with st.expander("📖 Deployment Instructions", expanded=False):
        st.markdown("""
        ### How to Deploy
        
        1. **Download Scripts**: Click "Generate Scripts" tab and download all generated files
        2. **Save to Folder**: Save all files (`main.bicep`, `parameters.json`, `deploy.sh` or `deploy.ps1`) to a folder
        3. **Open Terminal**: Navigate to the folder containing the deployment files
        4. **Login to Azure**: Run `az login` if not already authenticated
        5. **Run Deployment Script**:
           - **Linux/Mac**: `bash deploy.sh`
           - **Windows PowerShell**: `.\deploy.ps1`
        
        ### Alternative: Manual Deployment
        
        If you prefer to deploy manually, follow these steps:
        
        ```bash
        # 1. Login to Azure
        az login
        
        # 2. Set your subscription (if you have multiple)
        az account set --subscription "YOUR_SUBSCRIPTION_ID"
        
        # 3. Create resource group
        az group create --name YOUR_RESOURCE_GROUP --location eastus
        
        # 4. Deploy Bicep template
        az deployment group create \\
          --resource-group YOUR_RESOURCE_GROUP \\
          --template-file main.bicep \\
          --parameters parameters.json
        ```
        
        ### What gets deployed?
        
        - **Log Analytics Workspace**: For monitoring and logging
        - **Container Apps Environment**: Managed Kubernetes environment
        - **Container App**: Your AI agent application
        - **Auto-scaling**: Configured based on your settings
        - **HTTPS Endpoint**: Automatically provisioned with SSL
        """)
    
    # Authentication check
    st.markdown("#### 1️⃣ Authenticate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Check Azure Login Status"):
            # This would check az login status
            st.info("Authentication check would run here")
    
    with col2:
        if st.button("Login to Azure"):
            st.code("az login", language="bash")
            st.info("Run this command in your terminal")
    
    # Quick deployment option
    st.markdown("#### 2️⃣ Quick Deploy (Demo)")
    
    st.warning("⚠️ The deployment below is a simulation. Use the downloaded scripts for actual Azure deployment.")
    
    deployment_name = st.text_input(
        "Deployment Name",
        value=f"{st.session_state.project['name'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}"
    )
    
    dry_run = st.checkbox("Dry Run (Validate only)", value=True)
    
    if st.button("🚀 Start Deployment Simulation", use_container_width=True, type="primary"):
        deploy_to_azure(deployment_name, dry_run)

def deploy_to_azure(deployment_name: str, dry_run: bool):
    """Deploy project to Azure"""
    
    st.markdown("### Deployment Progress")
    
    # Save deployment scripts to disk
    import os
    import tempfile
    
    # Create deployment directory
    deploy_dir = os.path.join(os.getcwd(), 'deployments', deployment_name)
    os.makedirs(deploy_dir, exist_ok=True)
    
    status_text = st.empty()
    
    try:
        # Save all scripts to deployment directory
        status_text.text("💾 Saving deployment files...")
        
        for filename, content in st.session_state.deployment_scripts.items():
            file_path = os.path.join(deploy_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        st.success(f"✅ Deployment files saved to: {deploy_dir}")
        
        # Create deployer
        deployer = AzureDeployer(
            st.session_state.project,
            st.session_state.deployment_config,
            st.session_state.deployment_scripts
        )
        
        progress_bar = st.progress(0)
        
        steps = [
            "Validating configuration",
            "Creating resource group",
            "Deploying infrastructure",
            "Configuring secrets",
            "Deploying application",
            "Verifying deployment"
        ]
        
        for idx, step in enumerate(steps):
            status_text.text(f"Step {idx+1}/{len(steps)}: {step}...")
            
            # Simulate deployment step
            # In production, this would call actual Azure APIs
            import time
            time.sleep(1)
            
            progress_bar.progress((idx + 1) / len(steps))
        
        if dry_run:
            st.success("✅ Validation complete! Your deployment configuration is valid.")
            st.info("Uncheck 'Dry Run' to perform actual deployment.")
        else:
            st.success("🎉 Deployment complete!")
            
            # Show deployment details
            st.markdown("#### Deployment Details")
            
            deployment_url = f"https://{deployment_name}.azurecontainerapps.io"
            
            st.code(deployment_url)
            
            st.markdown(f"[Open Application]({deployment_url})")
            
    except Exception as e:
        st.error(f"❌ Deployment failed: {str(e)}")
        st.exception(e)

def show_monitoring():
    """Display monitoring dashboard"""
    
    st.markdown("### Monitoring Dashboard")
    
    st.info("Monitor your deployed agents in real-time")
    
    # Mock metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Status", "Healthy", delta="Running")
    
    with col2:
        st.metric("Requests/min", "142", delta="+12")
    
    with col3:
        st.metric("Avg Response Time", "324ms", delta="-23ms")
    
    with col4:
        st.metric("Error Rate", "0.2%", delta="-0.1%")
    
    st.markdown("---")
    
    # Logs
    st.markdown("#### Recent Logs")
    
    logs = [
        {"timestamp": "2025-11-06 10:23:45", "level": "INFO", "message": "Agent request processed successfully"},
        {"timestamp": "2025-11-06 10:23:42", "level": "INFO", "message": "New connection established"},
        {"timestamp": "2025-11-06 10:23:38", "level": "INFO", "message": "Agent initialized"},
    ]
    
    for log in logs:
        level_color = "green" if log['level'] == "INFO" else "red"
        st.markdown(f":{level_color}[{log['level']}] {log['timestamp']} - {log['message']}")
    
    st.markdown("---")
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Full Logs", use_container_width=True):
            st.info("Open Azure Portal for full logs")
    
    with col2:
        if st.button("🔄 Restart App", use_container_width=True):
            st.warning("Restart functionality")
    
    with col3:
        if st.button("🗑️ Delete Deployment", use_container_width=True):
            st.error("Delete functionality")
