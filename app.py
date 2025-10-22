import streamlit as st
import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Page setup ---
st.set_page_config(page_title="EduMentor AI", layout="centered")

# --- Load custom CSS & JS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("script.js") as f:
    st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header">
    <h1>🎓 <span class="gradient-text">EduMentor AI</span></h1>
    <p class="subtitle">Ask. Learn. Evolve. ✨</p>
</div>
""", unsafe_allow_html=True)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Quick Settings")
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
    st.markdown("<hr>", unsafe_allow_html=True)
    
# --- Chat history display ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# --- User input ---
prompt = st.chat_input("Ask your question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={"AIzaSyDDBVOqbjNyV2Bd3jsqvl4oRBbRSQXVrlE"}'
                headers = {"Content-Type": "application/json"}
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                reply = f"⚠️ Error: {e}"

            # Typing effect
            placeholder = st.empty()
            typed = ""
            for ch in reply:
                typed += ch
                placeholder.markdown(f"<div class='ai-msg typing'>{typed}</div>", unsafe_allow_html=True)
                time.sleep(0.012)
            placeholder.markdown(f"<div class='ai-msg'>{reply}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})