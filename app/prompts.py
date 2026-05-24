"""Prompt templates for AI Meeting Copilot."""


def build_meeting_summary_prompt(content: str) -> str:
    """Build the prompt used to summarize meeting notes."""
    return f"""
你是 AI 輔助的軟體工作流程整理助理。
請閱讀會議紀錄或需求內容，並用繁體中文產生以下內容：

1. 會議與需求摘要
2. TODO 清單
3. API 草稿
4. Markdown 知識筆記

會議紀錄或需求內容：
{content}
"""
