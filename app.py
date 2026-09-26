import streamlit as st
from google import genai
from google.genai import types

# --- 1. SET UP THE CHATBOT BRANDING ---
st.title("Custom AI Expert")
st.caption("A specialized conversational AI built with Streamlit and Gemini")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Google AI Studio API Key:", type="password")
    
    st.divider()
    st.header("Chatbot Behavior Configuration")
    
    # CHANGE THIS CHANGER BOX TO DEFINE ANY CHATBOT YOU WANT
    bot_persona = st.text_area(
        "System Prompt / Role Definition:",
        value="You are a professional software engineering mentor. Help the user debug code, write clean software, and understand complex algorithms step-by-step.",
        height=180
    )
    st.info("Get your free key at [Google AI Studio](https://google.com)")

# --- 2. AUTHENTICATION CHECK ---
if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to get started.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize client: {e}")
    st.stop()

# --- 3. CONVERSATION MEMORY MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display ongoing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. HANDLING INTERACTION & INFERENCE ---
if prompt := st.chat_input("Ask your specialized AI a question..."):
    # Render user query
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Query LLM with specific behavioral rules
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=bot_persona  # Injecting the logic parameters
                )
            )
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"API Error: {e}")
