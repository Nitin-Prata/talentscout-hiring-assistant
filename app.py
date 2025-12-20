"""
app.py

Streamlit entry point for the TalentScout Hiring Assistant.
Handles UI rendering and session management only.
"""

import streamlit as st

from chatbot.state import ConversationState
from chatbot.handlers import handle_user_input

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 TalentScout – Hiring Assistant")
st.caption("AI-powered initial screening for tech candidates")

# -------------------------
# Session State Initialization
# -------------------------
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = ConversationState()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

state: ConversationState = st.session_state.conversation_state

# -------------------------
# Display Chat History
# -------------------------
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# -------------------------
# Chat Input
# -------------------------
if not state.exit_flag:
    user_input = st.chat_input("Type your response here...")

    if user_input:
        # Display user message
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        # Process input through chatbot
        response = handle_user_input(user_input, state)

        # Display assistant response
        st.session_state.chat_history.append(("assistant", response))
        with st.chat_message("assistant"):
            st.write(response)
else:
    st.info("Conversation ended. Refresh the page to start a new session.")
