import streamlit as st
from groq import Groq
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Sohum AI", page_icon="🪯", layout="centered")

# --- 2. THE OG MODERN UI (Orange Glow & Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,600&family=Inter:wght@300;400;600&display=swap');
    
    /* Background & Global Font */
    .stApp { 
        background: radial-gradient(circle at top right, #1a1a1a, #050505); 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Elegant Saffron Header */
    .main-title { 
        font-family: 'Playfair Display', serif; 
        color: #FF9933; 
        font-size: 3.5rem; 
        text-align: center; 
        margin-bottom: 0px;
        text-shadow: 0 0 20px rgba(255, 153, 51, 0.3);
    }
    .sub-title { 
        color: #666; 
        font-size: 0.9rem; 
        text-align: center; 
        letter-spacing: 3px; 
        margin-bottom: 40px; 
        text-transform: uppercase;
    }

    /* Glassmorphism Chat Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 153, 51, 0.1) !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 15px !important;
    }
    
    /* Assistant Highlight */
    [data-testid="stChatMessageAssistant"] {
        border-left: 4px solid #FF9933 !important;
    }

    /* Glow Input Box */
    .stChatInputContainer {
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        background: rgba(0,0,0,0.2) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #FF9933 !important;
        box-shadow: 0 0 15px rgba(255, 153, 51, 0.2) !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY in Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sohum AI, a respectful and profound guide to Sikhism. Use 'Ji' for Gurus. Focus on the core pillars: Naam Japo, Kirat Karo, Vand Chakko. Be concise and poetic."}
    ]

# --- 4. UI LAYOUT ---
st.markdown('<h1 class="main-title">Sohum AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Wisdom • Oneness • Service</p>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color:#FF9933;'>🪯</h2>", unsafe_allow_html=True)
    st.write("Guided by the light of the Guru Granth Sahib Ji.")
    st.divider()
# --- 5. CHAT ENGINE ---
AI_ICON = "https://cdn-icons-png.flaticon.com/512/3244/3244673.png" # Saffron Icon URL
USER_ICON = "👤"

# Display History
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar=AI_ICON if msg["role"] == "assistant" else USER_ICON):
            st.markdown(msg["content"])

# Handle New Input
if prompt := st.chat_input("Ask a question about Sikhi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_ICON):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AI_ICON):
        placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.5
        )
        
        full_response = completion.choices[0].message.content
        
        # Smooth Typewriter Effect
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            placeholder.markdown(displayed_text + "▌")
            time.sleep(0.005)
        placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
