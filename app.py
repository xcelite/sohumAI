import streamlit as st
from groq import Groq
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Sohum AI | Finance", page_icon="📈", layout="centered")

# --- 2. THE CYBER-FINTECH UI (Modern & High-Tech) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Inter:wght@400;600&display=swap');
    
    .stApp { background: #05070a; font-family: 'Inter', sans-serif; }
    
    /* Neon Header */
    .title-text { font-family: 'Space Grotesk', sans-serif; color: #00ffa3; font-size: 3.5rem; font-weight: 700; text-align: center; margin-bottom: 0px; text-shadow: 0 0 20px rgba(0, 255, 163, 0.2); }
    .subtitle-text { color: #4e5d78; font-size: 0.9rem; text-align: center; margin-bottom: 40px; letter-spacing: 2px; text-transform: uppercase; }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] { background-color: rgba(10, 15, 24, 0.95) !important; border-right: 1px solid #1a202c; }

    /* Modern Finance Chips */
    .stButton > button {
        background: rgba(0, 255, 163, 0.05) !important;
        color: #00ffa3 !important;
        border: 1px solid rgba(0, 255, 163, 0.2) !important;
        border-radius: 12px !important;
        padding: 8px 15px !important;
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: #00ffa3 !important;
        color: #05070a !important;
        box-shadow: 0 0 15px rgba(0, 255, 163, 0.4);
    }

    /* Chat Styling */
    [data-testid="stChatMessage"] {
        background: rgba(16, 22, 32, 0.8) !important;
        border: 1px solid #232d3f !important;
        border-radius: 18px !important;
        margin-bottom: 15px !important;
    }
    
    /* AI Response Accent (Cyber Green) */
    [data-testid="stChatMessageAssistant"] { border-left: 4px solid #00ffa3 !important; }

    /* Input Field */
    .stChatInputContainer {
        border: 1px solid #232d3f !important;
        background: #0a0f18 !important;
        border-radius: 14px !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #00ffa3 !important;
        box-shadow: 0 0 20px rgba(0, 255, 163, 0.15) !important;
    }

    /* Metric Boxes */
    div[data-testid="metric-container"] {
        background: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & INITIALIZATION ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Secret Key Missing.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are Sohum AI, an elite financial intelligence agent for teenagers. 
        PURPOSE: Help teens master stock markets, compound interest, personal budgeting, and crypto.
        TONE: Highly advanced but clear. Use 'fin-tech' slang like 'bullish', 'DCA', 'APY', but explain them.
        FORMAT: Use bolding for numbers and ticker symbols. End with a sharp follow-up about a financial strategy."""}
    ]

# --- 4. THE UI LAYOUT ---
st.markdown('<h1 class="title-text">Sohum AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Financial Intelligence • Wealth Building • Stocks</p>', unsafe_allow_html=True)

# SIDEBAR: Financial Tools
with st.sidebar:
    st.markdown("<h2 style='color:#00ffa3;'>🛠️ Wealth Tools</h2>", unsafe_allow_html=True)
    st.write("Calculate your future net worth:")
    invest = st.number_input("Monthly Investment ($)", value=100)
    years = st.slider("Years to Grow", 1, 40, 10)
    rate = st.slider("Annual Return (%)", 1, 15, 8)
    
    # Compound Interest Formula
    future_value = invest * (((1 + (rate/100)/12)**(12*years) - 1) / ((rate/100)/12))
    st.metric("Estimated Wealth", f"${future_value:,.2f}", delta=f"{rate}% Return")
    st.divider()
    st.info("Sohum AI Guide: Remember, time in the market beats timing the market.")

# QUICK ACTIONS (Wisdom Chips)
st.markdown("<p style='text-align:center; color:#4e5d78; font-size:11px; font-weight:bold;'>MARKET COMMANDS</p>", unsafe_allow_html=True)
cols = st.columns(3)
quick_queries = ["🚀 How to start in Stocks?", "💎 What is an Index Fund?", "📉 Bull vs Bear Market?"]

if "query_trigger" not in st.session_state:
    st.session_state.query_trigger = None

for i, query in enumerate(quick_queries):
    if cols[i].button(query):
        st.session_state.query_trigger = query

# --- 5. CHAT ENGINE ---
AI_ICON = "⚡"
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
        response_placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.3
        )
        
        full_response = completion.choices[0].message.content
        
        # Smooth Streaming Effect
        displayed_text = ""
        for char in full_response:
            displayed_text += char
            response_placeholder.markdown(displayed_text + "▌")
            time.sleep(0.001)
        response_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if st.session_state.query_trigger:
    handle_input(st.session_state.query_trigger)
    st.session_state.query_trigger = None
    st.rerun()

if prompt := st.chat_input("Analyze a ticker or ask a finance question..."):
    handle_input(prompt)
