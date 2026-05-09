"""Streamlit UI for AI Meeting Copilot."""

import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/summarize")


st.set_page_config(
    page_title="AI Meeting Assistance",
    page_icon="AI",
    layout="wide",
)

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
    color: #e5e7eb;
}

.block-container {
    padding: 2.5rem 4rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.22);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
    padding-left: 1.4rem;
    padding-right: 1.4rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #e5e7eb !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(148, 163, 184, 0.18);
    margin-top: 2rem;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 6px;
}

.hero-subtitle {
    font-size: 15px;
    color: #93c5fd;
    margin-bottom: 28px;
}

.metric-card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 20px;
    padding: 22px 28px;
    min-height: 136px;
}

.section-label {
    font-size: 13px;
    color: #38bdf8;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    color: #f8fafc;
}

.output-box {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px;
    min-height: 470px;
    color: #dbeafe;
}

.output-box p,
.output-box li {
    color: #dbeafe;
}

.rag-box {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 16px;
    padding: 16px 18px;
    margin-top: 18px;
}

.rag-title {
    color: #38bdf8;
    font-weight: 700;
    margin-bottom: 8px;
}

.stTextArea textarea {
    background-color: #020617;
    color: #dbeafe;
    border-radius: 16px;
    border: 1px solid #334155;
    font-size: 15px;
}

.stTextArea textarea::placeholder {
    color: #93c5fd !important;
    opacity: 1 !important;
}

.stTextArea textarea:focus {
    border: 1px solid #e5e7eb;
    box-shadow: 0 0 0 1px #e5e7eb;
}

div[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.95) !important;
    border: 1px solid rgba(56, 189, 248, 0.28) !important;
    border-radius: 14px !important;
    color: #e5e7eb !important;
}

div[data-baseweb="select"] span {
    color: #e5e7eb !important;
    font-weight: 500 !important;
}

div[data-baseweb="select"] svg {
    fill: #94a3b8 !important;
}

span[data-baseweb="tag"] {
    background: linear-gradient(90deg, #2563eb, #06b6d4) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

span[data-baseweb="tag"] span {
    color: #ffffff !important;
}

ul[role="listbox"] {
    background-color: #020617 !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
}

li[role="option"] {
    background-color: #020617 !important;
    color: #e5e7eb !important;
}

li[role="option"]:hover {
    background-color: #1e293b !important;
    color: #38bdf8 !important;
}

.stButton button {
    background: linear-gradient(90deg, #2563eb, #06b6d4);
    color: white;
    border-radius: 14px;
    height: 52px;
    font-weight: 700;
    border: none;
    padding-left: 18px;
    padding-right: 18px;
}

.stButton button:hover {
    background: linear-gradient(90deg, #1d4ed8, #0891b2);
    color: white;
}

[data-testid="stExpander"] {
    background-color: rgba(2, 6, 23, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-title">AI Requirement Copilot</div>
<div class="hero-subtitle">
Transform messy meeting notes into structured requirements, tasks, API drafts, and reusable knowledge notes.
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## ⚙️ Control Panel")

    input_type = st.selectbox(
        "Source Type",
        ["PM需求", "會議紀錄", "Bug討論", "API變更需求", "系統設計"],
    )

    output_type = st.multiselect(
        "Output Modules",
        ["需求摘要", "TODO", "API Draft", "Knowledge Note"],
        default=["需求摘要", "TODO", "API Draft", "Knowledge Note"],
    )

    st.markdown("---")
    st.caption("AI-assisted software workflow workspace.")

left, right = st.columns([0.85, 1.15], gap="large")

with left:
    st.markdown(
        """
    <div class="metric-card">
        <div class="section-label">Input</div>
        <div class="card-title">Meeting / Requirement Source</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    meeting_text = st.text_area(
        "Paste content",
        height=420,
        label_visibility="collapsed",
        placeholder="貼上 PM 需求、會議紀錄、bug 討論或 API 變更需求...",
    )

    analyze = st.button("Analyze Requirement")

with right:
    st.markdown(
        """
    <div class="metric-card">
        <div class="section-label">AI Output</div>
        <div class="card-title">Structured Workflow Result</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if analyze:
        if not meeting_text.strip():
            st.warning("請先輸入內容")
        else:
            try:
                with st.spinner("AI 正在整理需求並查詢知識庫..."):
                    response = requests.post(
                        API_URL,
                        json={
                            "content": meeting_text,
                            "source_type": input_type,
                            "output_modules": output_type,
                        },
                        timeout=90,
                    )

                response.raise_for_status()
                payload = response.json()
                result = payload.get("result", "")
                related_knowledge = payload.get("related_knowledge", [])

                st.markdown('<div class="output-box">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(
                    '<div class="rag-box"><div class="rag-title">RAG Retrieved Knowledge Notes</div>',
                    unsafe_allow_html=True,
                )
                if related_knowledge:
                    for item in related_knowledge:
                        source = item.get("source", "unknown")
                        distance = item.get("distance")
                        with st.expander(f"{source} · distance {distance:.4f}" if isinstance(distance, float) else source):
                            st.markdown(item.get("content", ""))
                else:
                    st.info("沒有找到相關 knowledge note")
                st.markdown("</div>", unsafe_allow_html=True)

            except requests.exceptions.RequestException as exc:
                st.error(f"API 呼叫失敗：{exc}")
    else:
        st.markdown(
            """
        <div class="output-box">
        <p>分析結果會顯示在這裡。</p>
        <br>
        <p>建議輸入 PM 需求、會議紀錄或 bug 討論，系統會整理成：</p>
        <ul>
            <li>需求摘要</li>
            <li>開發 TODO</li>
            <li>API Draft</li>
            <li>Knowledge Note</li>
        </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )
