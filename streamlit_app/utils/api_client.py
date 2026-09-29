"""
API client for communicating with the FastAPI RAG backend.
"""

import logging

import requests

logger = logging.getLogger(__name__)

# FastAPI RAG backend
# PYTHON_BASE_URL = "http://127.0.0.1:8000"

RUST_BASE_URL = "http://localhost:8080/api"


import os

PYTHON_BASE_URL = os.getenv(
    "PYTHON_BASE_URL",
    "http://127.0.0.1:8000"
)

def query_backend(query: str, session_id: str) -> str:
    """
    Send a query to the RAG backend.
    """
    url = f"{PYTHON_BASE_URL}/rag/query"
    logger.info("Calling RAG backend: %s", url)

    try:
        response = requests.post(
            url,
            json={
                "query": query,
                "session_id": session_id,
            },
        )

        if response.status_code == 200:
            return response.json()["result"]["content"]

        return f"Error: {response.status_code} - {response.text}"

    except requests.RequestException as e:
        logger.exception("RAG query failed: %s", e)
        return f"Connection error: {e}"


def document_upload_rag(file, description: str) -> bool:
    """
    Upload a document to the RAG system.
    """
    headers = {
        "X-Description": description
    }

    url = f"{PYTHON_BASE_URL}/rag/documents/upload"

    try:
        if file:
            files = {
                "file": (file.name, file, file.type)
            }

            response = requests.post(
                url,
                files=files,
                headers=headers,
            )

            logger.info(
                "Document upload status: %s",
                response.status_code
            )

            return response.status_code == 200

        return False

    except requests.RequestException as e:
        logger.exception("Document upload failed: %s", e)
        return False