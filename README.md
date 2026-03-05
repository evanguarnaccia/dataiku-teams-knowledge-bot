# 🤖 Dataiku AI-Powered Microsoft Teams Knowledge Bot

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Dataiku](https://img.shields.io/badge/Dataiku-14.4-00B2A9)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 Executive Summary
This project establishes a secure, enterprise-grade Retrieval-Augmented Generation (RAG) pipeline that allows users to query internal company documentation directly through Microsoft Teams. By integrating Azure AI Search with the Dataiku LLM Mesh, the bot provides "grounded" answers—meaning it only responds based on authorized PDF documentation, significantly reducing AI hallucinations and ensuring data privacy.

![Dataiku Teams Bot Architecture Diagram](docs/AzureBotTeamsLLM.png)

## 🏗️ Architectural Workflow
The system operates across three primary platforms, as illustrated in the provided architecture diagram:

### 1. User Interface & Communication (Microsoft 365)
* **Microsoft Teams:** Serves as the front-end interface where users interact with the bot.
* **Azure Bot Service:** Acts as the secure gateway, handling authentication via Azure Active Directory (AAD) and routing messages between Teams and the Dataiku backend.

### 2. Data Processing & Orchestration (Dataiku Platform)
* **Webhook Listener (Python Backend):** A Dataiku-hosted Flask application that serves as the "brain." It receives secure HTTP POST requests from Azure, processes user intent, and orchestrates the RAG flow.
* **Dataiku Answers API / LLM Mesh:** The core orchestration layer that connects the backend to specific AI models and knowledge bases.
* **Knowledge Bank (RAG):** A Dataiku-managed object that points to an Azure AI Search Index. This index contains PDF documents pre-parsed by Azure Document Intelligence, converted into Markdown, and vectorized for semantic search.

### 3. Intelligence Layer (External LLM Provider)
* **External LLM (OpenAI/Azure OpenAI):** The "Generation" component. It receives a curated prompt containing the user's question and the specific document snippets retrieved from the Knowledge Bank.

## 🛠️ Technical Implementation Details

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Document Parsing** | Azure Document Intelligence | Converts complex PDFs into structured Markdown. |
| **Vector Database** | Azure AI Search | Stores document embeddings for high-speed semantic retrieval. |
| **Orchestration** | Dataiku 14.4 LLM Mesh | Manages model connections and RAG Knowledge Banks. |
| **Backend** | Python (Flask) | Handles the Microsoft Bot Framework JSON schema and Auth. |
| **Security** | Oauth2 / Client Credentials | Ensures only authorized Teams users can trigger the bot. |

## 🛡️ Key Benefits & Guardrails
* **Grounded Responses:** The bot is configured with a strict system prompt to answer only from the provided context. If an answer isn't in the docs, it will say so, preventing misinformation.
* **Automatic Citations:** Every response includes a "Sources" footer, allowing users to verify the information against the original PDF filename.
* **Scalability:** New documents can be added to the Azure Search Index without modifying a single line of code in the Teams bot.

---

## 🚀 Getting Started

### Prerequisites
* **Dataiku DSS** version 14.4+ (with LLM Mesh enabled).
* **Microsoft Azure** account with active Azure Bot Service and Azure AI Search resources.
* **Microsoft Teams** environment with sideloading/custom app permissions enabled.

### Quick Start Installation
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_ORGANIZATION/dataiku-teams-knowledge-bot.git](https://github.com/YOUR_ORGANIZATION/dataiku-teams-knowledge-bot.git)
   cd dataiku-teams-knowledge-bot


