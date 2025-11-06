Build a powerful AI single or multi-agent builder canvas using Microsoft Agent Framework (MAF) integrated with any vector database and LLM models (Azure AI Services, OpenAI, etc.). The solution should support click-and-drag functionality with configurable data source connections, models, and prompt customization. The goal is to enable creation of enterprise-grade, secure, and deployable agents with clear instructions and usage guides.
Key Features to Include:


Visual Builder for MAF Solutions

Prompt-to-canvas flow: Capture a product brief on the landing page and jump straight into the studio with the chat seeded.
Document-grounded prompts: Attach docs or images, select existing tools, and hand off context-aware instructions to the generator.



Drag-and-Drop Authoring

Compose agents, team managers, and function/MCP tools.
Include validation tailored to the export pipeline.



Live Preview Sandbox

Spin up a WebContainers backend in the browser for smoke-testing flows without leaving the workspace.



Playbooks & Scenes

Save reusable multi-agent templates with placeholder slots.
Load templates into new projects easily.



Evaluation Harness

Define scripted conversations with assertions.
Exported bundles should include the QA suite.


Deployment & Authentication

Azure deploy button: Generate a ready-to-run CLI script using bundled Bicep templates for Container Apps deployment.
Sign in with GitHub, Microsoft Entra (Azure AD), or email magic links to sync projects and scenarios.