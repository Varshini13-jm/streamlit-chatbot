import streamlit as st
import os

from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(
    page_title="Your AI Assistant",
    page_icon="🤖",
    layout="centered"
)

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

system_message = {
    "role": "system",
    "content": "You are a friendly AI assistant who explains things clearly and simply."
}

st.title("My AI Chatbot 🤖")

if len(st.session_state.messages) == 0:
    st.info(
        "👋 Welcome! Try asking me about Python, AI, or anything you're curious about."
    )

with st.sidebar:

    st.header("About")

    st.write(
        "This chatbot was built using Streamlit and OpenRouter."
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"): # user bubble
        st.write(user_input) # to display user input

    with st.spinner("⏳Thinking..."):

       response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[system_message] + st.session_state.messages
       )

       answer = response.choices[0].message.content

       st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
      )

       with st.chat_message("assistant"): #assisstant bubble
         st.write(answer)# to display assistant response