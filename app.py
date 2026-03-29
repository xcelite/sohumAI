import streamlit as st
from groq import Groq

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Sikhism AI", page_icon="🪯", layout="centered")

# --- 2. THE ELITE UI (CSS) ---
st.markdown("""
    <style>
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    /* Main Background & Font */
    .stApp { 
        background-color: #050505; 
        font-family: 'Inter', sans-serif;
    }

    /* Professional Header */
    .main-title {
        color: #FF9933;
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #666;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        background-color: #0e0e0e !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    /* AI Response Accent */
    [data-testid="stChatMessageAssistant"] {
        border-left: 4px solid #FF9933 !important;
    }

    /* Glowing Input Box Customization */
    .stChatInputContainer {
        padding: 10px !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid #222 !important;
        border-radius: 16px !important;
        transition: all 0.4s ease;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #FF9933 !important;
        box-shadow: 0 0 20px rgba(255, 153, 51, 0.25) !important;
    }

    /* Hide unnecessary Streamlit UI elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* User Avatar Styling */
    [data-testid="stChatMessageUser"] .st-emotion-cache-1edm7bh {
        background-color: #1B3A6B !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API INITIALIZATION ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("Missing GROQ_API_KEY in Secrets.")
    st.stop()

# --- 4. APP LAYOUT ---
st.markdown('<p class="main-title">Sikhism Wisdom AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Explore the history, values, and teachings of the Gurus.</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a master guide to Sikhism. RULES: Be CONCISE (max 150 words). Direct answer first. Use 'Ji' for Gurus. Bold key terms. End with one curious follow-up question."}
    ]

# Display Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Ask your heart..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            # Using the 70B model for high intelligence
            response_container = st.empty()
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.4
            )
            full_response = completion.choices[0].message.content
            response_container.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error calling Groq: {e}")
