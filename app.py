import streamlit as st
from groq import Groq
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Sikhism AI Guide", page_icon="🪯")

# --- CUSTOM MODERN CSS (Restored your glowing UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stChatMessage"] { 
        background-color: #111111 !important; 
        border-left: 3px solid #FF9933 !important;
        border-radius: 10px;
    }
    .stChatInputContainer {
        border: 1px solid #333 !important;
        border-radius: 15px !important;
    }
    /* The Glow Effect */
    .stChatInputContainer:focus-within {
        border-color: #FF9933 !important;
        box-shadow: 0 0 15px rgba(255, 153, 51, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
# On Vercel, we use os.environ to get your Secret Key
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a master guide to Sikhism. Be CONCISE. Direct answer first. Use 'Ji' for Gurus. Bold key terms. End with a 1-sentence follow-up."}
    ]

# Display history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about Sikhi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.4
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
