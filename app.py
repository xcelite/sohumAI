import streamlit as st
from groq import Groq
import time

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="Sohum AI | Fintech", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
    
    .stApp { background: #05070a; font-family: 'Inter', sans-serif; }
    
    .main-header { 
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem; font-weight: 800; color: #00ffa3; 
        text-align: center; margin-bottom: 0px;
        text-shadow: 0 0 30px rgba(0, 255, 163, 0.2);
    }

    /* Jargon Glow Card - Specific highlight for analogies */
    .jargon-box {
        background: rgba(0, 255, 163, 0.05);
        border: 1px dashed #00ffa3;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    [data-testid="stChatMessage"] {
        background: #0d1117 !important;
        border: 1px solid #1e293b !important;
        border-radius: 16px !important;
    }
    
    [data-testid="stChatMessageAssistant"] {
        border-left: 5px solid #00ffa3 !important;
    }

    .stChatInputContainer { border-radius: 15px !important; border: 1px solid #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE GEN-Z FINTECH ENGINE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are Sohum AI, a high-level Financial Intelligence Agent for teens.
        
        CORE RULE: Use the 'Gen-Z Filter'. Never sound like a bank brochure. 
        When explaining complex jargon, use 'Fluent Fintech' analogies:
        - Liquidity = Cash vs. V-Bucks/Skins (Can't buy pizza with a skin).
        - Volatility = A TikTok sound's hype cycle (Huge peak, then falls off).
        - Diversification = Not putting all your eggs in one Discord server.
        - Inflation = When the rare skins everyone wanted suddenly become common/cheap.
        
        FORMAT: 
        1. Give the professional definition.
        2. Use a 'Translation' section with a relatable analogy.
        3. Keep it punchy. Use bolding for Tickers and Gains."""}
    ]

# --- 3. INITIALIZATION ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Check your GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# --- 4. UI LAYOUT ---
st.markdown('<h1 class="main-header">Sohum AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#4e5d78; font-weight:600; letter-spacing:2px;'>FINANCIAL INTELLIGENCE AGENT</p>", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### 🛠️ Mode: Fluent Fintech")
    st.success("Gen-Z Filter: ACTIVE")
    st.divider()
    st.markdown("### 💡 Pro Tip")
    st.info("Ask me: 'Explain Options trading like I'm 5' or 'What is a Short Squeeze in Fortnite terms?'")

# QUICK START CHIPS
cols = st.columns(3)
chips = ["💧 What is Liquidity?", "📉 Explain Volatility", "🏦 Why use an HYSA?"]
if "trigger" not in st.session_state: st.session_state.trigger = None

for i, text in enumerate(chips):
    if cols[i].button(text, use_container_width=True):
        st.session_state.trigger = text

# --- 5. CHAT LOGIC ---
def process_chat(text):
    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)

    with st.chat_message("assistant", avatar="⚡"):
        placeholder = st.empty()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.5
        )
        full_res = response.choices[0].message.content
        
        # Fast "Matrix" Stream
        curr = ""
        for char in full_res:
            curr += char
            placeholder.markdown(curr + "▌")
            time.sleep(0.001)
        placeholder.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})

# Display history
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"], avatar="⚡" if m["role"] == "assistant" else None):
            st.markdown(m["content"])

if st.session_state.trigger:
    process_chat(st.session_state.trigger)
    st.session_state.trigger = None
    st.rerun()

if prompt := st.chat_input("Drop a finance question..."):
    process_chat(prompt)
