import streamlit as st
import time

# Page configuration for multi-device styling
st.set_page_config(page_title="Nexus AI Web App", layout="wide")

# Custom CSS for Dark Theme (Nexus Style)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #8a2be2; font-size: 28px; }
    </style>
""", unsafe_allow_html=True)

# Left Sidebar Navigation
st.sidebar.title("🤖 Nexus Automator V2")
menu = st.sidebar.radio("MAIN MENU", ["Dashboard", "Bulk Image Generator", "Text to Speech"])

if menu == "Dashboard":
    st.title("🎬 Seedance Vid Gen")
    
    # Top 4 Metric Cards (Nexus Vibe)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="TOTAL PROMPTS", value="0")
    with col2: st.metric(label="QUEUED", value="0")
    with col3: st.metric(label="GENERATING", value="0")
    with col4: st.metric(label="DONE", value="0")
    
    st.markdown("---")
    
    # Main Grid Layout (Left Side Setup, Right Side Prompt Input)
    left_side, right_side = st.columns([1, 2])
    
    with left_side:
        st.subheader("⚙️ GENERATION SETTINGS")
        model = st.selectbox("MODEL", ["Seedance 2.0", "Veo 3.1"])
        duration = st.slider("DURATION (SECONDS)", 5, 15, 15)
        aspect_ratio = st.selectbox("ASPECT RATIO", ["9:16", "16:9", "1:1"])
        batch_size = st.number_input("BATCH SIZE", min_value=1, max_value=50, value=10)
        
        st.button("🚀 START GENERATION", use_container_width=True)
        st.button("🛑 STOP GENERATION", use_container_width=True)
        
    with right_side:
        st.subheader("📝 PROMPTS QUEUE")
        prompts_input = st.text_area(
            "Paste your bulk prompts here (One prompt per line):", 
            height=300,
            placeholder="An orange squirrel surfing on a wave...\nA modern futuristic cyberpunk city at night..."
        )

# Simple footer for access
st.sidebar.markdown("---")
st.sidebar.info("Authorized Mobile/PC Session Active")
