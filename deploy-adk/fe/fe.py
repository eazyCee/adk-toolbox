
#  Copyright 2025 Google LLC
 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
 
#       https://www.apache.org/licenses/LICENSE-2.0
 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import streamlit as st
import requests

# --- Configuration ---
import os
API_URL = os.environ.get("API_URL")
USER_ID = ""
COMPANY = ""

# --- Initialize session state variables ---
# 'messages' will store the chat history: list of {"role": "user/assistant", "content": "..."}
if "messages" not in st.session_state:
    st.session_state.messages = []
# 'session_id' will store the current session ID from the API
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# --- App Title ---
st.title("Simple Chatbot")

# --- Helper function to call the chatbot API ---
def get_chatbot_response(query: str, current_session_id: str = None):
    """
    Sends a query to the chatbot API and returns the response and new session_id.
    """
    payload = {
        "query": query,
        "user_id": USER_ID,
        "company": COMPANY
    }
    if current_session_id:
        payload["session_id"] = current_session_id

    try:
        response = requests.post(API_URL, json=payload, timeout=30) # Added timeout
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        return data.get("response"), data.get("session_id")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return f"Sorry, I encountered an error connecting to the service: {e}", current_session_id # Keep old session_id on error
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return f"Sorry, an unexpected error occurred: {e}", current_session_id


# --- "Refresh Session" Button ---
# Placing it at the top for easy access
if st.button("🔄 Refresh Session"):
    st.session_state.messages = []
    st.session_state.session_id = None
    st.success("Session refreshed! Start a new conversation.")
    # st.rerun() # Optional: force immediate clear, usually not needed if state change is handled correctly

# --- Display existing chat messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and "Submit" (handled by st.chat_input) ---
if prompt := st.chat_input("What is your question?"):
    # 1. Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get bot response
    with st.spinner("Assistant is thinking..."): # Show a thinking indicator
        bot_response_text, new_session_id = get_chatbot_response(
            query=prompt,
            current_session_id=st.session_state.session_id
        )

    # 3. Update session_id in state
    st.session_state.session_id = new_session_id

    # 4. Add bot response to chat history and display it
    st.session_state.messages.append({"role": "assistant", "content": bot_response_text})
    with st.chat_message("assistant"):
        st.markdown(bot_response_text)

# --- For Debugging: Show current session_id (optional) ---
# st.sidebar.subheader("Debug Info")
# st.sidebar.write(f"Current Session ID: {st.session_state.session_id}")
# st.sidebar.write("Current Messages:")
# st.sidebar.json(st.session_state.messages)