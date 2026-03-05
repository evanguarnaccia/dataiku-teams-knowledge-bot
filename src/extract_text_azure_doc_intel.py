import dataiku
import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION
# ==========================================
# This loads the variables from your hidden .env file
load_dotenv() 

# This securely pulls them into your script
AZURE_ENDPOINT = os.environ.get("AZURE_DOC_INTEL_ENDPOINT")
AZURE_KEY = os.environ.get("AZURE_DOC_INTEL_KEY")

if not AZURE_KEY:
    raise ValueError("Missing Azure Document Intelligence Key! Check your environment variables.")

# We use the 'prebuilt-layout' model and request Markdown output
API_VERSION = "2024-02-29-preview"
ANALYZE_URL = f"{AZURE_ENDPOINT.rstrip('/')}/documentintelligence/documentModels/prebuilt-layout:analyze?api-version={API_VERSION}&outputContentFormat=markdown"

HEADERS = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Content-Type": "application/pdf"
}

# ==========================================
# 2. DATAIKU SETUP
# ==========================================
# Replace these with your actual Dataiku folder and dataset names
input_folder = dataiku.Folder("pdf_bank")
output_dataset = dataiku.Dataset("prepared_docs")

extracted_data = []

# ==========================================
# 3. PROCESSING LOOP
# ==========================================
paths = input_folder.list_paths_in_partition()

for path in paths:
    if not path.lower().endswith('.pdf'):
        continue
        
    print(f"Processing: {path}...")
    
    # Read the PDF directly from the Dataiku folder
    with input_folder.get_download_stream(path) as stream:
        pdf_bytes = stream.read()
        
    # Step A: Send the PDF to Azure
    response = requests.post(ANALYZE_URL, headers=HEADERS, data=pdf_bytes)
    
    if response.status_code != 202:
        print(f"Error submitting {path}: {response.text}")
        continue
        
    # Azure processes documents asynchronously. It gives us a URL to check the status.
    poll_url = response.headers["Operation-Location"]
    
    # Step B: Poll Azure until the extraction is finished
    status = "running"
    while status in ["running", "notStarted"]:
        time.sleep(3) # Wait 3 seconds between checks
        poll_response = requests.get(poll_url, headers={"Ocp-Apim-Subscription-Key": AZURE_KEY})
        poll_data = poll_response.json()
        status = poll_data.get("status")
        
    # Step C: Extract the Markdown
    if status == "succeeded":
        markdown_text = poll_data["analyzeResult"]["content"]
        extracted_data.append({
            "filename": os.path.basename(path),
            "markdown_content": markdown_text
        })
        print(f"Success: {path}")
    else:
        print(f"Failed to process {path}: {status}")

# ==========================================
# 4. SAVE TO DATAIKU DATASET
# ==========================================
if extracted_data:
    df = pd.DataFrame(extracted_data)
    output_dataset.write_with_schema(df)
    print("All documents processed and saved to dataset!")
else:
    print("No data extracted.")
