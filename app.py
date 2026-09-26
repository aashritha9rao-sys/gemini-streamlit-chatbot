import streamlit as st

st.title("AI Chatbot")

# Create a text input field for user input
user_input = st.text_input("Ask me something")

# Create a submit button
if st.button("Send"):
    if user_input.strip():
        # Display the text entered by the user
        st.success(f"You entered: {user_input}")
    else:
        st.warning("Please enter some text first.")