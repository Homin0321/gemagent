# app.py
import streamlit as st
import requests
import json
import uuid

# Set Streamlit page configuration
st.set_page_config(page_title="ADK API Frontend", layout="wide")

# Sidebar: Agent settings
st.sidebar.header("Agent Settings")
api_url = st.sidebar.text_input("API Server URL", "http://localhost:8000")  # API endpoint input
agent_name = st.sidebar.text_input("Agent Name", "allinone")  # Agent name input
user_id = "user"  # Fixed user ID

# Sidebar: Session and response control buttons
create_session_button = st.sidebar.button("Create New Session", width="stretch")  # Button to create a new session
show_full_response = st.sidebar.button("Show Full Response", width="stretch")  # Button to show full API response

# Session state: Track if a session is created
if "session_created" not in st.session_state:
    st.session_state.session_created = False

def create_new_session(api_url, agent_name, user_id):
    """
    Create a new session and handle the deletion of existing session.
    Returns tuple of (success, session_id, error_message)
    """
    try:
        # Delete previous session if it exists
        if "session_id" in st.session_state:
            old_session_id = st.session_state.session_id
            delete_url = f"{api_url}/apps/{agent_name}/users/{user_id}/sessions/{old_session_id}"
            delete_res = requests.delete(delete_url)
            # Changed to accept both 200 and 204 as successful deletion
            if delete_res.status_code not in [200, 204]:
                return False, None, f"Failed to delete existing session: {delete_res.status_code}"

        # Create a new session with a new session ID
        session_id = uuid.uuid4().hex
        url = f"{api_url}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
        res = requests.post(url)
        
        if res.status_code == 200:
            return True, session_id, None
        else:
            return False, None, f"Session creation failed: {res.status_code}\n{res.text}"
    except Exception as e:
        return False, None, f"Error during session creation: {e}"

# Automatically create a session if not already created
if not st.session_state.session_created:
    success, session_id, error = create_new_session(api_url, agent_name, user_id)
    if success:
        st.session_state.session_created = True
        st.session_state.session_id = session_id
    else:
        st.error(error)

# When "Create New Session" button is pressed
if create_session_button:
    success, session_id, error = create_new_session(api_url, agent_name, user_id)
    if success:
        st.session_state.session_created = True
        st.session_state.session_id = session_id
        st.session_state.chat_history = []  # Clear chat history
        if "last_response" in st.session_state:
            del st.session_state.last_response  # Clear last response
        st.rerun()  # Refresh the Streamlit app
    else:
        st.error(error)

# Initialize chat history in session state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display all previous chat messages from chat history
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box for user to enter a new question
query_text = st.chat_input("Enter your question")

if query_text:
    # If session is not created, warn the user
    if not st.session_state.session_created:
        st.warning("Please create a session first.")
    else:
        # Add user message to chat history and display it
        st.session_state.chat_history.append({"role": "user", "content": query_text})
        st.chat_message("user").write(query_text)

        session_id = st.session_state.session_id
        # Prepare payload for API request
        payload = {
            "app_name": agent_name,
            "user_id": user_id,
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": query_text}]
            }
        }
        # Send user message to backend API
        res = requests.post(f"{api_url}/run", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.session_state.last_response = data  # Save full response for later viewing
            if len(data) >= 1:
                # Get the last message from the response array
                final_text = data[-1]["content"]["parts"][0].get("text", "")
                # Add assistant's reply to chat history and display it
                st.session_state.chat_history.append({"role": "assistant", "content": final_text})
                st.chat_message("assistant").write(final_text)
        else:
            st.error(f"Query failed: {res.status_code}")
            st.text(res.text)

# Dialog to show the full JSON response from the backend
@st.dialog("📜 Full Response JSON", width="large")
def show_json_dialog():
    if "last_response" in st.session_state:
        st.json(st.session_state.last_response)
    else:
        st.write("No response data available.")

# Show the full response dialog when the button is pressed
if show_full_response:
    show_json_dialog()