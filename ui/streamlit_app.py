"""Streamlit UI for AI Meeting Assistance."""

import html
import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/summarize")
HISTORY_URL = os.getenv("HISTORY_URL", API_URL.rsplit("/", 1)[0] + "/history")


st.set_page_config(
    page_title="AI Meeting Assistance",
    page_icon="AI",
    layout="wide",
)

st.markdown(
    """
<style>
#MainMenu,
header,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

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

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(2, 6, 23, 0.45);
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 12px;
    margin-bottom: 8px;
    padding: 10px 12px;
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
    border-radius: 14px;
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
    border-radius: 14px;
    padding: 20px;
    color: #dbeafe;
}

.output-box p,
.output-box li {
    color: #dbeafe;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px;
    color: #dbeafe;
}

[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li,
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
    color: #dbeafe;
}

.rag-box {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 18px;
}

.rag-title {
    color: #38bdf8;
    font-weight: 700;
    margin-bottom: 8px;
}

.history-section {
    margin-top: 6px;
}

.history-list {
    margin-top: 18px;
}

.history-item {
    background: rgba(2, 6, 23, 0.68);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
}

.history-date {
    color: #93c5fd;
    font-size: 13px;
    margin-bottom: 8px;
}

.history-content {
    color: #e5e7eb;
}

.pager-status {
    color: #93c5fd;
    font-size: 14px;
    font-weight: 700;
    text-align: center;
    padding-top: 16px;
}

.stTextArea textarea {
    background-color: #020617;
    color: #dbeafe;
    border-radius: 14px;
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
<div class="hero-title">AI Meeting Assistance</div>
<div class="hero-subtitle">
將會議紀錄、需求訪談與 Bug 回報整理成需求摘要、TODO、API 草稿與可重複使用的知識筆記。
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 控制面板")

    page = st.radio("頁面", ["輸入輸出", "歷史紀錄"], label_visibility="collapsed")

    st.markdown("---")
    st.caption("AI 輔助的軟體工作流程整理工具。")

if page == "輸入輸出":
    left, right = st.columns([0.85, 1.15], gap="large")

    with left:
        st.markdown(
            """
        <div class="metric-card">
            <div class="section-label">輸入</div>
            <div class="card-title">會議與需求來源</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        meeting_text = st.text_area(
            "貼上內容",
            height=420,
            label_visibility="collapsed",
            placeholder="貼上 PM 需求、會議紀錄、Bug 回報或 API 需求...",
        )

        analyze = st.button("開始分析")

    with right:
        st.markdown(
            """
        <div class="metric-card">
            <div class="section-label">AI 輸出</div>
            <div class="card-title">結構化工作流程結果</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if analyze:
            if not meeting_text.strip():
                st.warning("請先貼上要分析的內容。")
            else:
                try:
                    with st.spinner("AI 正在整理需求內容..."):
                        response = requests.post(
                            API_URL,
                            json={"content": meeting_text},
                            timeout=90,
                        )

                    response.raise_for_status()
                    payload = response.json()
                    result = payload.get("result", "")
                    related_knowledge = payload.get("related_knowledge", [])

                    with st.container(border=True):
                        st.markdown(result)

                    st.markdown(
                        '<div class="rag-box"><div class="rag-title">RAG 檢索到的知識筆記</div>',
                        unsafe_allow_html=True,
                    )
                    if related_knowledge:
                        for item in related_knowledge:
                            source = item.get("source", "未知來源")
                            distance = item.get("distance")
                            label = (
                                f"{source} - 距離 {distance:.4f}"
                                if isinstance(distance, float)
                                else source
                            )
                            with st.expander(label):
                                st.markdown(item.get("content", ""))
                    else:
                        st.info("沒有找到相關的知識筆記。")
                    st.markdown("</div>", unsafe_allow_html=True)

                except requests.exceptions.RequestException as exc:
                    st.error(f"API 請求失敗：{exc}")
        else:
            with st.container(border=True):
                st.markdown(
                    """
等待輸入來源內容。

貼上 PM 需求、會議紀錄或 Bug 回報後，可產生：

- 需求摘要
- TODO
- API 草稿
- 知識筆記
"""
                )

else:
    st.markdown('<div class="history-section">', unsafe_allow_html=True)
    st.markdown(
        """
    <div class="metric-card">
        <div class="section-label">歷史紀錄</div>
        <div class="card-title">近期分析紀錄</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    try:
        history_response = requests.get(HISTORY_URL, timeout=10)
        history_response.raise_for_status()
        history_items = history_response.json()

        if history_items:
            page_size = 10
            total_pages = max(1, (len(history_items) + page_size - 1) // page_size)
            current_page = min(st.session_state.get("history_page", 1), total_pages)
            st.session_state.history_page = current_page

            start_index = (current_page - 1) * page_size
            end_index = start_index + page_size
            page_items = history_items[start_index:end_index]

            st.markdown('<div class="history-list">', unsafe_allow_html=True)
            for item in page_items:
                created_at = html.escape(item.get("created_at", ""))
                content = item.get("content", "")
                ai_result = item.get("ai_result", "")
                preview = html.escape(content[:220] + ("..." if len(content) > 220 else ""))

                st.markdown(
                    f"""
    <div class="history-item">
        <div class="history-date">{created_at}</div>
        <div class="history-content">{preview}</div>
    </div>
    """,
                    unsafe_allow_html=True,
                )
                with st.expander("查看結果"):
                    st.markdown(ai_result)
            st.markdown("</div>", unsafe_allow_html=True)

            previous_col, status_col, next_col = st.columns([1, 1.4, 1])
            with previous_col:
                if st.button("上一頁", disabled=current_page <= 1, use_container_width=True):
                    st.session_state.history_page = current_page - 1
                    st.rerun()
            with status_col:
                selected_page = st.selectbox(
                    "頁碼選擇",
                    range(1, total_pages + 1),
                    index=current_page - 1,
                    format_func=lambda page_number: f"第 {page_number} / {total_pages} 頁",
                    label_visibility="collapsed",
                )
                if selected_page != current_page:
                    st.session_state.history_page = selected_page
                    st.rerun()
            with next_col:
                if st.button("下一頁", disabled=current_page >= total_pages, use_container_width=True):
                    st.session_state.history_page = current_page + 1
                    st.rerun()
        else:
            st.info("目前沒有分析紀錄。")
    except requests.exceptions.RequestException:
        st.info("API 伺服器啟動後才能讀取歷史紀錄。")

    st.markdown("</div>", unsafe_allow_html=True)
