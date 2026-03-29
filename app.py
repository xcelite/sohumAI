import streamlit as st
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Sikhism AI", page_icon="🪯", layout="centered")

# 2. Modern Dark CSS
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage { background: #131313 !important; border-left: 4px solid #FF9933 !important; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stChatInput"] { border: 1px solid #333; border-radius: 15px; background: rgba(255,255,255,0.05); }
    div[data-testid="stChatInput"]:focus-within { border-color: #FF9933; box-shadow: 0 0 15px rgba(255, 153, 51, 0.3); }
    </style>
    """, unsafe_allow_html=True)

st.title("🪯 Sikhism Wisdom AI")

# 3. Setup Client (Using Secrets for Security)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a master guide to Sikhism. Be CONCISE (max 150 words). Use 'Ji' for Gurus. Bold key terms. End with a 1-sentence follow-up."}]

# 4. Display Chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Chat Input
if prompt := st.chat_input("Ask about the Gurus, History, or Values..."):
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
