import dataiku
from flask import request
import requests

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Microsoft Teams Config
TENANT_ID = ""
APP_ID = ""
APP_PASSWORD = "" # Remember to rotate this later!

# Dataiku LLM Mesh & Knowledge Bank Config
LLM_ID = "openai:evan-openai-connection:gpt-5.2" 
KB_ID = "Jfb5N4aq" # e.g., "my_new_kb"

@app.route('/teams-webhook', methods=['POST'])
def teams_webhook():
    activity = request.json
    
    # Ignore non-message events
    if activity.get('type') != 'message':
        return "OK", 200

    user_text = activity.get('text', '').strip()
    if not user_text:
        return "OK", 200

    # ==========================================
    # 2. QUERY DATAIKU KNOWLEDGE BANK (RAG)
    # ==========================================
    try:
        # --- STEP A: RETRIEVAL ---
        # 1. Access the Knowledge Bank as a LangChain Vector Store
        kb = dataiku.KnowledgeBank(id=KB_ID)
        vector_store = kb.as_langchain_vectorstore()
        
        # 2. Search the Knowledge Bank for the best matching chunks (k=3 results)
        search_results = vector_store.similarity_search(user_text, k=3)
        
        # 3. Extract the text and filenames from the results
        context_snippets = []
        sources = set()
        
        for doc in search_results:
            content = doc.page_content
            # Dataiku stores your Title/Source column inside the metadata dictionary
            filename = doc.metadata.get("filename", "Internal Document")
            
            context_snippets.append(f"Source: {filename}\nContent: {content}")
            sources.add(filename)
            
        joined_context = "\n\n".join(context_snippets)

        # --- STEP B: GENERATION ---
        # 4. Generate the answer using the LLM Mesh
        client = dataiku.api_client()
        project = client.get_default_project()
        llm = project.get_llm(LLM_ID)
        
        completion = llm.new_completion()
        
        system_prompt = (
            "You are a helpful Dataiku assistant. Answer the user's question using ONLY the context provided below. "
#            "If the answer is not contained in the context, say 'I cannot find the answer in the provided documents.'\n\n"
            "If the answer is not contained in the context, you may use your general knowledge to answer.'\n\n"
            f"CONTEXT:\n{joined_context}"
        )
        
        completion.with_message(system_prompt, role="system")
        completion.with_message(user_text, role="user")
        
        llm_response = completion.execute()
        bot_text = llm_response.text if llm_response.success else "Failed to generate answer."
        
        # 5. Append citations cleanly
        if sources and "cannot find the answer" not in bot_text.lower():
            bot_text += f"\n\n**Sources:** {', '.join(sources)}"
                
    except Exception as e:
        bot_text = f"Knowledge Bank Error: {str(e)}"
        print(f"Error Details: {str(e)}")
        
    # ==========================================
    # 3. PUSH REPLY TO MICROSOFT TEAMS
    # ==========================================
    auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": APP_ID,
        "client_secret": APP_PASSWORD,
        "scope": "https://api.botframework.com/.default"
    }
    
    token_res = requests.post(auth_url, data=auth_data)
    if token_res.status_code != 200:
        print(f"Auth Error: {token_res.text}")
        return "Auth Failed", 500
        
    token = token_res.json().get("access_token")

    service_url = activity.get('serviceUrl')
    conversation_id = activity.get('conversation', {}).get('id')
    activity_id = activity.get('id')
    
    reply_url = f"{service_url}v3/conversations/{conversation_id}/activities/{activity_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    reply_payload = {
        "type": "message",
        "text": bot_text,
        "from": activity.get("recipient"),
        "recipient": activity.get("from"),
        "replyToId": activity_id
    }

    reply_res = requests.post(reply_url, json=reply_payload, headers=headers)
    print(f"Microsoft Reply Status: {reply_res.status_code}")
    
    return "OK", 200
