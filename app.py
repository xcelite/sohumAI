import streamlit as st
from groq import Groq
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Sikhism AI", page_icon="🪯", layout="centered")

# --- 2. THE PREMIUM CSS (Modern & Attractive) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
    
    .stApp { background: linear-gradient(135deg, #050505 0%, #0a0a0a 100%); font-family: 'Inter', sans-serif; }
    
    /* Elegant Header */
    .title-text { font-family: 'Playfair Display', serif; color: #FF9933; font-size: 3rem; margin-bottom: 0px; text-align: center; }
    .subtitle-text { color: #666; font-size: 1rem; text-align: center; margin-bottom: 40px; letter-spacing: 1px; }

    /* Wisdom Chips / Buttons */
    .stButton > button {
        background: rgba(255, 153, 51, 0.05) !important;
        color: #FF9933 !important;
        border: 1px solid rgba(255, 153, 51, 0.3) !important;
        border-radius: 20px !important;
        padding: 5px 20px !important;
        transition: all 0.3s ease !important;
        font-size: 13px !important;
    }
    .stButton > button:hover {
        background: rgba(255, 153, 51, 0.2) !important;
        border-color: #FF9933 !important;
        transform: translateY(-2px);
    }

    /* Chat Styling */
    [data-testid="stChatMessage"] {
        background: rgba(18, 18, 18, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #222 !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        margin-bottom: 15px !important;
    }
    
    /* Glowing Input */
    .stChatInputContainer {
        border: 1px solid #333 !important;
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        transition: border 0.4s ease, box-shadow 0.4s ease;
    }
    .stChatInputContainer:focus-within {
        border-color: #FF9933 !important;
        box-shadow: 0 0 25px rgba(255, 153, 51, 0.2) !important;
    }

    /* Avatar Circles */
    [data-testid="stChatMessage"] .st-emotion-cache-1edm7bh { border: 2px solid #FF9933; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & INITIALIZATION ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please set GROQ_API_KEY in Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a master guide to Sikhism. Be concise, respectful, and modern. Use 'Ji' for Gurus. Bold key terms. End with one question."}
    ]

# --- 4. THE UI LAYOUT ---
st.markdown('<h1 class="title-text">Sohum AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">WISDOM • HISTORY • SERVICE</p>', unsafe_allow_html=True)

# IDEA #2: WISDOM CHIPS (Quick Actions)
st.markdown("<p style='text-align:center; color:#444; font-size:12px;'>EXPLORE TOPICS</p>", unsafe_allow_html=True)
cols = st.columns(3)
quick_queries = ["✨ Guru Nanak Dev Ji", "⚔️ Meaning of Khalsa", "📜 The Five Ks"]

# We use a session state trick to "click" buttons into the chat
if "query_trigger" not in st.session_state:
    st.session_state.query_trigger = None

for i, query in enumerate(quick_queries):
    if cols[i].button(query):
        st.session_state.query_trigger = query

# --- 5. CHAT ENGINE ---
# Standard icons or URL to custom Sikh-themed icons
AI_ICON = "https://cdn-icons-png.flaticon.com/512/3244/3244673.png" # Example Khanda-style icon
USER_ICON = "👤"

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar=AI_ICON if msg["role"] == "assistant" else USER_ICON):
            st.markdown(msg["content"])

def handle_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=USER_ICON):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=AI_ICON):
        # IDEA #5 (Extra): STREAMING EFFECT
        response_placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.4
        )
        
        full_response = completion.choices[0].message.content
        
        # Simulate streaming for that "modern AI" feel
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            response_placeholder.markdown(displayed_text + "▌")
            time.sleep(0.002) # Fast stream
        response_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Check if a Wisdom Chip was clicked
if st.session_state.query_trigger:
    handle_input(st.session_state.query_trigger)
    st.session_state.query_trigger = None
    st.rerun()

# Regular Chat Input
if prompt := st.chat_input("Ask your heart..."):
    handle_input(prompt)

# --- 6. SIDEBAR (The Final Modern Touch) ---
with st.sidebar:
    st.markdown("<h2 style='color:#FF9933;'>🪯 About Sohum</h2>", unsafe_allow_html=True)
    st.info("Sohum AI is a respectful guide to Sikh philosophy and history, powered by Llama 3.3.")
    st.divider()
    st.markdown("### Daily Fact")
    st.write("**Seva** (Selfless Service) is one of the three pillars of Sikhism. Over 100,000 people eat for free daily at the Golden Temple.")
