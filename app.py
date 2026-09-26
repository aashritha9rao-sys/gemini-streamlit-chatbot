import streamlit as st
import time
from google import genai
from google.genai.errors import APIError  # For catching specific Google API errors

st.title("My Gemini Chatbot")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Google AI Studio API Key:", type="password")
    st.info("You can get a free key from [Google AI Studio](https://aistudio.google.com/)")

if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to get started.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize client: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is on your mind?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # --- RETRY LOGIC FOR 503 OVERLOADS ---
        max_retries = 3
        retry_delay = 2  # start with a 2-second delay
        full_response = ""
        
        for attempt in range(max_retries):
            try:
                # Call the updated official Gemini model natively
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )
                full_response = response.text
                break  # Success! Break out of the loop.
                
            except APIError as e:
                # If it's a 503 server overload, wait and try again
                if e.code == 503 and attempt < max_retries - 1:
                    message_placeholder.warning(f"Google servers busy. Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Wait twice as long next time (4s, then 8s)
                else:
                    # Give up if it's a different error or we ran out of retries
                    full_response = f"API Error: {e.message}"
                    break
            except Exception as e:
                full_response = f"An unexpected error occurred: {e}"
                break
        
        # Clear out any temporary warning boxes and show final text
        message_placeholder.empty()
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
