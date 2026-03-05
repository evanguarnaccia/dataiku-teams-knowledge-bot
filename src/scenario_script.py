import dataiku
from dataiku.scenario import Scenario
import time

# ==========================================
# 1. CONFIGURATION
# ==========================================
SOURCE_FOLDER_ID = "" # Keep your actual 8-char ID here!
DOC_INTEL_RECIPE = "compute_prepared_docs"
EMBEDDING_RECIPE = "compute_prepared_docs_embedded"

scenario = Scenario()
client = dataiku.api_client()
project = client.get_default_project()

# Helper function to poll the job status
def wait_for_job(job, recipe_name):
    print(f"Waiting for {recipe_name} to complete...")
    while True:
        # The job status dictionary contains the current state
        state = job.get_status().get('baseStatus', {}).get('state', '')
        
        if state == 'DONE':
            print(f"Success: {recipe_name} finished!")
            return True
        elif state in ['FAILED', 'ABORTED']:
            print(f"Error: {recipe_name} stopped with state: {state}")
            return False
            
        time.sleep(5) # Wait 5 seconds before pinging the server again

# ==========================================
# 2. EXECUTION LOGIC
# ==========================================
try:
    folder = project.get_managed_folder(SOURCE_FOLDER_ID)
    contents = folder.list_contents()
    
    if not contents.get('items'):
        print(f"Folder {SOURCE_FOLDER_ID} is empty. Cancelling scenario.")
        scenario.cancel("No files to process.")
    else:
        print(f"Found {len(contents['items'])} files. Starting RAG update pipeline...")

        # STEP 1: Run Document Intelligence
        print(f"Starting Step 1: {DOC_INTEL_RECIPE}...")
        job_1 = project.get_recipe(DOC_INTEL_RECIPE).run()
        
        if not wait_for_job(job_1, DOC_INTEL_RECIPE):
            raise Exception(f"{DOC_INTEL_RECIPE} failed. Check the Dataiku Jobs tab.")

        # STEP 2: Run Embedding
        print(f"Starting Step 2: {EMBEDDING_RECIPE}...")
        job_2 = project.get_recipe(EMBEDDING_RECIPE).run()
        
        if not wait_for_job(job_2, EMBEDDING_RECIPE):
            raise Exception(f"{EMBEDDING_RECIPE} failed. Check the Dataiku Jobs tab.")

        print("Update Successful: Both recipes finished and the Knowledge Bank is current.")

except Exception as e:
    print(f"Scenario Error: {str(e)}")
    raise e
