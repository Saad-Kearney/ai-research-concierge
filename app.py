import streamlit as st
import os
import requests
from dotenv import load_dotenv
from docx import Document
from io import BytesIO

# Load local .env (if exists)
load_dotenv()

# Use local .env OR cloud secret
together_api_key = os.getenv("TOGETHER_API_KEY") or st.secrets["TOGETHER_API_KEY"]

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {together_api_key}",
    "Content-Type": "application/json"
}

# Page config
st.set_page_config(page_title="ARC – AI Research Concierge", layout="wide")

# Header
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(
        """
        <h1 style='color:#7823DC;'>Welcome to ARC – AI Research Concierge</h1>
        <h4 style='color:#7823DC; margin-top:-10px;'>by KEARNEY</h4>
        <p style='font-size:16px;'>
            <i>Your personal AI assistant for generating consulting-grade slide structures and Point-of-View (PoV) outlines – faster, smarter, and more structured.</i>
        </p>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.image("kearney_logo.png", width=200)

# Topic + model
col1, col2 = st.columns([4, 1])
with col1:
    if "topic" not in st.session_state:
        st.session_state.topic = ""

    if st.session_state.topic == "":
        st.markdown("<p style='font-weight:bold; font-size:18px;'>Enter a research topic</p>", unsafe_allow_html=True)
        st.session_state.topic = st.text_input("", placeholder="e.g., Future of AI in retail banking")
    else:
        st.text_input("Enter a research topic", value=st.session_state.topic, disabled=True)

with col2:
    model_option = st.selectbox("Choose model", [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "togethercomputer/llama-2-70b-chat"
    ], index=0)

MODEL = model_option

# Generate
if st.session_state.topic and "summary" not in st.session_state and st.button("Generate Insights"):
    with st.spinner("Thinking like a consultant..."):

        # SOURCES
        prompt_sources = f"List 10 reliable sources or publication types to study the topic: {st.session_state.topic}"
        sources_body = {
            "model": MODEL,
            "max_tokens": 1000,
            "temperature": 0.3,
            "messages": [{"role": "user", "content": prompt_sources}]
        }
        r_sources = requests.post(API_URL, headers=HEADERS, json=sources_body)
        st.session_state.sources = r_sources.json()['choices'][0]['message']['content'].strip()

        # SUMMARY
        prompt_summary = f"Summarize the key insights about: {st.session_state.topic} for a consulting analyst."
        summary_body = {
            "model": MODEL,
            "max_tokens": 1000,
            "temperature": 0.3,
            "messages": [{"role": "user", "content": prompt_summary}]
        }
        r_summary = requests.post(API_URL, headers=HEADERS, json=summary_body)
        st.session_state.summary = r_summary.json()['choices'][0]['message']['content'].strip()

        # POV
        prompt_pov = (
            f"As a strategy consultant, outline a slide-by-slide Point-of-View deck on the topic: "
            f"'{st.session_state.topic}'. Include slide titles and key content for each."
        )
        pov_body = {
            "model": MODEL,
            "max_tokens": 1000,
            "temperature": 0.3,
            "messages": [{"role": "user", "content": prompt_pov}]
        }
        r_pov = requests.post(API_URL, headers=HEADERS, json=pov_body)
        st.session_state.pov = r_pov.json()['choices'][0]['message']['content'].strip()

# Display
if "summary" in st.session_state and "sources" in st.session_state and "pov" in st.session_state:
    st.markdown("<h2 style='color:#7823DC;'>🔗 Suggested Sources</h2>", unsafe_allow_html=True)
    st.write(st.session_state.sources)

    st.markdown("<h2 style='color:#7823DC;'>📄 Summary</h2>", unsafe_allow_html=True)
    st.write(st.session_state.summary)

    st.markdown("<h2 style='color:#7823DC;'>📊 Point-of-View Structure</h2>", unsafe_allow_html=True)
    st.write(st.session_state.pov)

    # Export Word
    st.markdown("<h2 style='color:#7823DC;'>⬇️ Export Report</h2>", unsafe_allow_html=True)
    doc = Document()
    doc.add_heading("AI Research Concierge Report", level=1)
    doc.add_paragraph(f"Topic: {st.session_state.topic}")
    doc.add_heading("Suggested Sources", level=2)
    doc.add_paragraph(st.session_state.sources)
    doc.add_heading("Summary", level=2)
    doc.add_paragraph(st.session_state.summary)
    doc.add_heading("Point-of-View Structure", level=2)
    doc.add_paragraph(st.session_state.pov)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📄 Download as Word (.docx)",
        data=buffer,
        file_name=f"AI_Research_{st.session_state.topic.replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # Reset
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Explore another topic"):
        for key in ["topic", "summary", "sources", "pov"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
