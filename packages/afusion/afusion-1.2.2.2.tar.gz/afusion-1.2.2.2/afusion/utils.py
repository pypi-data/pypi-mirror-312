# utils.py

import os
import uuid
import json
import requests
from loguru import logger
import streamlit as st

def log_to_ga():
    # Replace with your Measurement ID
    measurement_id = "G-42P6TDX7LH"
    # Get API secret from environment variable
    api_secret = "Z-CSzz9hSsK3MSaxJjB8sQ"

    if not api_secret:
        logger.error("API secret for Google Analytics not found. Please set the GA_API_SECRET environment variable.")
        return

    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

    # Generate or retrieve a unique client ID for each user session
    if 'client_id' not in st.session_state:
        st.session_state['client_id'] = str(uuid.uuid4())

    client_id = st.session_state['client_id']
    logger.debug(f"Client ID: {client_id}")

    payload = {
        "client_id": client_id,
        "events": [{
            "name": "app_start",
            "params": {}
        }]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 204:
            logger.error(f"Failed to log to Google Analytics: {response.content}")
        else:
            logger.info("Successfully logged to Google Analytics")
    except Exception as e:
        logger.error(f"Exception occurred while logging to Google Analytics: {e}")

def compress_output_folder(output_folder_path, job_output_folder_name):
    import os
    import zipfile
    import io
    from loguru import logger

    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=output_folder_path)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    logger.debug(f"Compressed output folder: {output_folder_path}")
    return zip_buffer.getvalue()
