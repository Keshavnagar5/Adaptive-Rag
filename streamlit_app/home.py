"""
Home page for LangGraph Assistant.
"""

import streamlit as st

# Hide sidebar navigation
hide_sidebar_style = """
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
"""

st.set_page_config(
    page_title="LangGraph Assistant",
    page_icon="🤖",
    layout="wide",
)

st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.title("🤖 Welcome to LangGraph Assistant")

st.write(
    "Your Adaptive RAG assistant is ready. "
    "Upload documents and ask questions using the chat interface."
)

if st.button("🚀 Start Chat", use_container_width=True):
    st.switch_page("pages/chat.py")