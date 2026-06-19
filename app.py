import streamlit as st
import replicate
import os
import time

# Page configuration
st.set_page_config(page_title="Nexus AI Cloud", layout="wide")

# Custom Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #8a2be2; font-size: 28px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Left Sidebar
st.sidebar.title("🤖 Nexus Automator V2")

# API Token Key Secure Input Box
api_key = st.sidebar.text_input("🔑 Enter Replicate API Token:", type="password")
if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key

menu = st.sidebar.radio("MAIN MENU", ["Dashboard", "Bulk Image Generator", "Text to Speech"])

if menu == "Dashboard":
    st.title("🎬 Seedance Vid Gen")
    
    # Session States to track metrics dynamically
    if 'total' not in st.session_state: st.session_state.total = 0
    if 'queued' not in st.session_state: st.session_state.queued = 0
    if 'generating' not in st.session_state: st.session_state.generating = 0
    if 'done' not in st.session_state: st.session_state.done = 0
    if 'video_links' not in st.session_state: st.session_state.video_links = []

    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("TOTAL PROMPTS", st.session_state.total)
    with col2: st.metric("QUEUED", st.session_state.queued)
    with col3: st.metric("GENERATING", st.session_state.generating)
    with col4: st.metric("DONE", st.session_state.done)
    
    st.markdown("---")
    
    left_side, right_side = st.columns([1, 2])
    
    with left_side:
        st.subheader("⚙️ GENERATION SETTINGS")
        model_type = st.selectbox("MODEL", ["Seedance 2.0 Fast ($0.04/s)", "Veo 3.1"])
        duration = st.slider("DURATION (SECONDS)", 5, 15, 15)
        aspect_ratio = st.selectbox("ASPECT RATIO", ["9:16", "16:9", "1:1"])
        
        start_btn = st.button("🚀 START GENERATION", use_container_width=True)
        
    with right_side:
        st.subheader("📝 PROMPTS QUEUE")
        prompts_input = st.text_area(
            "Paste bulk prompts here (One prompt per line):", 
            height=200,
            placeholder="An orange squirrel surfing on a wave...\nA futuristic dark psychology scene..."
        )

    # Core Execution Logic
    if start_btn:
        if not api_key:
            st.error("❌ Pehle Sidebar mein apna Replicate API Token daalein!")
        elif not prompts_input.strip():
            st.error("❌ Khas baat! Pehle prompts queue mein kuch prompts likhein.")
        else:
            # Process prompt list split by lines
            lines = [l.strip() for l in prompts_input.split('\n') if l.strip()]
            st.session_state.total = len(lines)
            st.session_state.queued = len(lines)
            st.session_state.generating = 0
            
            # Loop through each prompt just like Nexus Automator
            for idx, current_prompt in enumerate(lines):
                st.session_state.queued -= 1
                st.session_state.generating = 1
                st.toast(f"Generating video {idx+1}/{st.session_state.total}...")
                
                try:
                    # Hitting the background Seedance/Fast Cloud engine
                    output = replicate.run(
                        "bytedance/seedance-2.0", 
                        input={
                            "prompt": current_prompt,
                            "duration": duration,
                            "aspect_ratio": aspect_ratio,
                            "audio": False # Disabling audio saves 50% cash
                        }
                    )
                    video_url = output[0] if isinstance(output, list) else output
                    st.session_state.video_links.append((current_prompt, video_url))
                    st.session_state.done += 1
                except Exception as e:
                    st.error(f"Error on prompt {idx+1}: {e}")
                
                st.session_state.generating = 0
            st.success("🎉 Saari Bulk Videos Successfully Ban Chuki Hain!")

    # Display generated output down below
    if st.session_state.video_links:
        st.markdown("### 📥 GENERATED VIDEOS OUTPUT")
        for p, link in st.session_state.video_links:
            st.write(f"**Prompt:** {p}")
            st.video(link)
            st.markdown(f"[🔗 Download Video]({link})")
            st.markdown("---")
        
