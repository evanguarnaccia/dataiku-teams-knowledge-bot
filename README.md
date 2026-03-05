# 🤖 Dataiku AI-Powered Microsoft Teams Knowledge Bot

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Dataiku](https://img.shields.io/badge/Dataiku-14.4-00B2A9)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 Executive Summary
[cite_start]This project establishes a secure, enterprise-grade Retrieval-Augmented Generation (RAG) pipeline that allows users to query internal company documentation directly through Microsoft Teams[cite: 3]. [cite_start]By integrating Azure AI Search with the Dataiku LLM Mesh, the bot provides "grounded" answers[cite: 4]. [cite_start]It only responds based on authorized PDF documentation, significantly reducing AI hallucinations and ensuring data privacy[cite: 4].


## 🏗️ Architectural Workflow
[cite_start]The system operates across three primary platforms[cite: 33]:

### 1. User Interface & Communication (Microsoft 365)
* [cite_start]**Microsoft Teams:** Serves as the front-end interface where users interact with the bot[cite: 35].
* [cite_start]**Azure Bot Service:** Acts as the secure gateway, handling authentication via Azure Active Directory (AAD) and routing messages between Teams and the Dataiku backend[cite: 36].

### 2. Data Processing & Orchestration (Dataiku Platform)
* [cite_start]**Webhook Listener (Python Backend):** A Dataiku-hosted Flask application that serves as the "brain"[cite: 40]. [cite_start]It receives secure HTTP POST requests from Azure, processes user intent, and orchestrates the RAG flow[cite: 41].
* [cite_start]**Dataiku Answers API / LLM Mesh:** The core orchestration layer that connects the backend to specific AI models and knowledge bases[cite: 42].
* [cite_start]**Knowledge Bank (RAG):** A Dataiku-managed object that points to an Azure AI Search Index[cite: 43]. [cite_start]This index contains PDF documents pre-parsed by Azure Document Intelligence, converted into Markdown, and vectorized for semantic search[cite: 44].

### 3. Intelligence Layer (External LLM Provider)
* [cite_start]**External LLM:** The "Generation" component[cite: 46]. [cite_start]It receives a curated prompt containing the user's question and the specific document snippets retrieved from the Knowledge Bank[cite: 46].

## 🛠️ Technical Implementation Details

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Document Parsing** | Azure Document Intelligence | [cite_start]Converts complex PDFs into structured Markdown[cite: 48]. |
| **Vector Database** | Azure AI Search | [cite_start]Stores document embeddings for high-speed semantic retrieval[cite: 48]. |
| **Orchestration** | Dataiku 14.4 LLM Mesh | [cite_start]Manages model connections and RAG Knowledge Banks[cite: 48]. |
| **Backend** | Python (Flask) | [cite_start]Handles the Microsoft Bot Framework JSON schema and Auth[cite: 48]. |
| **Security** | Oauth2 / Client Credentials | [cite_start]Ensures only authorized Teams users can trigger the bot[cite: 48]. |

## 🛡️ Key Benefits & Guardrails
* [cite_start]**Grounded Responses:** The bot is configured with a strict system prompt to answer only from the provided context[cite: 51]. [cite_start]If an answer isn't in the docs, it will say so, preventing misinformation[cite: 52].
* [cite_start]**Automatic Citations:** Every response includes a "Sources" footer, allowing users to verify the information against the original PDF filename[cite: 53].
* [cite_start]**Scalability:** New documents can be added to the Azure Search Index without modifying a single line of code in the Teams bot[cite: 54].

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
