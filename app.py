import streamlit as st
import pandas as pd
import time

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="Sohum AI | War Room", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #05070a; font-family: 'Inter', sans-serif; }
    .war-room-header { 
        font-family: 'Space Grotesk', sans-serif;
        color: #ff4b4b; font-size: 2.5rem; font-weight: 800; text-align: center;
    }
    .strategy-card {
        background: rgba(255, 75, 75, 0.05);
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    [data-testid="stMetric"] { background: #0d1117; border: 1px solid #232d3f; padding: 15px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DEBT LOGIC ENGINE ---
def calculate_crush_map(debts, extra_payment, strategy):
    # Sort based on Logic
    if strategy == "Avalanche (Mathematical Logic)":
        debts = sorted(debts, key=lambda x: x['rate'], reverse=True)
    else: # Snowball (Psychological Logic)
        debts = sorted(debts, key=lambda x: x['balance'])
    
    # Simple simulation of 10-year interest savings
    total_interest_saved = sum([d['balance'] * (d['rate']/100) * 10 for d in debts]) * (extra_payment / 500)
    return debts, total_interest_saved

# --- 3. THE WAR ROOM UI ---
st.markdown('<h1 class="war-room-header">DEBT-CRUSH WAR ROOM</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>STOP PAYING INTEREST. START OWNING YOUR FUTURE.</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛡️ Strategy Intel")
    strat = st.radio("Choose Your Logic:", ["Avalanche (Mathematical Logic)", "Snowball (Psychological Logic)"])
    st.divider()
    st.info("💡 **Avalanche:** Targets highest interest first. Saves the most money.\n\n🔥 **Snowball:** Targets smallest balance first. Wins the psychological game.")

# Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Input Your Debts")
    with st.expander("Add Debt Items", expanded=True):
        d1_name = st.text_input("Debt Name", "Student Loan A")
        d1_bal = st.number_input("Balance ($)", value=5000)
        d1_rate = st.number_input("Interest Rate (%)", value=6.5)
        
        st.divider()
        extra = st.slider("Monthly Extra 'Crush' Payment ($)", 0, 1000, 100)

# Process Logic
debt_list = [{"name": d1_name, "balance": d1_bal, "rate": d1_rate}]
# Adding a dummy second debt for visual mapping
debt_list.append({"name": "Credit Card", "balance": 1200, "rate": 22.0})

mapped_debts, savings = calculate_crush_map(debt_list, extra, strat)

with col2:
    st.subheader("🗺️ Dynamic Strategy Map")
    
    # Metrics
    m1, m2 = st.columns(2)
    m1.metric("10-Year Interest Saved", f"${savings:,.2f}", delta="Crushing It", delta_color="normal")
    m2.metric("Next Target", mapped_debts[0]['name'])

    # The Map
    st.markdown('<div class="strategy-card">', unsafe_allow_html=True)
    st.markdown(f"### 🎯 CURRENT OBJECTIVE: {mapped_debts[0]['name']}")
    st.write(f"Every extra **${extra}** you have this month goes directly here. Do not spread it thin. Focus fire until this balance is $0.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualizing the "Hit List"
    st.write("### ⚔️ The Hit List (Priority Order)")
    for i, d in enumerate(mapped_debts):
        st.write(f"**{i+1}. {d['name']}** | Balance: ${d['balance']} | Rate: {d['rate']}%")

# --- 4. CHAT AGENT (Logic Focused) ---
st.divider()
st.subheader("🧠 Discuss Strategy with Sohum AI")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are Sohum AI. Focus on Debt-Crush logic. Explain the math of interest like a trap that we are escaping."}]

if prompt := st.chat_input("Ask about the logic..."):
    with st.chat_message("user"): st.write(prompt)
    # [Insert Groq API call here to handle the response]
    with st.chat_message("assistant"): st.write("Based on the Avalanche Logic, your Credit Card is a 'Financial Leak'. By plugging that leak first, you effectively give yourself a 22% guaranteed return on your money.")
