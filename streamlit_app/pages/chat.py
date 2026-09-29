"""
Chat page for the Streamlit Adaptive RAG application.
"""

import uuid

import streamlit as st

from utils.api_client import (
    query_backend,
    document_upload_rag,
)

# Configure page
st.set_page_config(
    page_title="LangGraph Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create a session ID for this browser session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header
st.title("💬 LangGraph Adaptive RAG")

st.caption(
    "Ask questions about your uploaded documents or use the Adaptive RAG agent."
)

# Sidebar - Document upload
with st.sidebar:
    st.header("📂 Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload a PDF or TXT file",
        type=["pdf", "txt"],
    )

    if uploaded_file:
        file_description = st.text_input(
            "📄 Describe your document",
            max_chars=300,
            placeholder="E.g. LangGraph tutorial with workflows and code examples",
        )

        if file_description:

            if "uploaded_files" not in st.session_state:
                st.session_state.uploaded_files = set()

            file_key = f"{uploaded_file.name}_{file_description}"

            if file_key not in st.session_state.uploaded_files:

                if st.button("📤 Upload Document", use_container_width=True):

                    success = document_upload_rag(
                        uploaded_file,
                        file_description,
                    )

                    if success:
                        st.success(
                            f"Uploaded: {uploaded_file.name}"
                        )

                        st.session_state.uploaded_files.add(
                            file_key
                        )

                    else:
                        st.error(
                            f"Document upload failed: {uploaded_file.name}"
                        )

            else:
                st.success(
                    f"Already uploaded: {uploaded_file.name}"
                )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Display previous messages
for role, text in st.session_state.chat_history:

    with st.chat_message(role):
        st.markdown(text)

# Chat input
user_input = st.chat_input(
    "Ask a question about your documents..."
)

if user_input:

    # Display user message immediately
    st.session_state.chat_history.append(
        ("user", user_input)
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Query FastAPI RAG backend
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = query_backend(
                user_input,
                st.session_state.session_id,
            )

            st.markdown(response)

    # Save response
    st.session_state.chat_history.append(
        ("assistant", response)
    )
