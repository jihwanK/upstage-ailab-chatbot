import streamlit as st
from chatbot import Chatbot
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize chatbot instance
chatbot = Chatbot(llm_platform="openai")

def init_session_state():
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

def main():
    st.title("🍯   푸와   친구들의   고민상담   🍯")
    st.divider()

    init_session_state()

    if st.session_state.username is None or st.session_state.username.strip() == "":
        username_input = st.text_input("이름을 입력해 주세요")
        if username_input:
            st.session_state.username = username_input.strip()
            st.experimental_rerun()

    if st.session_state.username and st.session_state.username.strip() != "":
        messages = st.container()

        # Display conversation messages
        for chat in st.session_state.conversation:
            messages.chat_message("user").write(chat['user'])
            messages.chat_message("assistant").write(chat['bot'])

        # Chat input box at the bottom of the page
        prompt = st.chat_input("메시지를 입력해 주세요")
        if prompt:
            try:
                response = chatbot._chat(prompt, st.session_state.username)
                st.session_state.conversation.append({"user": prompt, "bot": response})
                st.experimental_rerun()  # Rerun the app to update the conversation display
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
