"""FastAPI entry point for AI Meeting Copilot."""

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel, Field

from app.config import get_openai_api_key, is_openai_configured
from app.db import get_history, init_db, save_meeting
from app.rag import search_knowledge


app = FastAPI(title="AI Meeting Copilot")
init_db()


class MeetingInput(BaseModel):
    """Input payload for meeting summarization."""

    content: str = Field(..., min_length=1)


class KnowledgeResult(BaseModel):
    """A knowledge note retrieved by the RAG search."""

    source: str
    content: str
    distance: float


class SummaryOutput(BaseModel):
    """Output payload for meeting summarization."""

    result: str
    related_knowledge: list[KnowledgeResult]


class HistoryItem(BaseModel):
    """A saved meeting summary."""

    id: int
    content: str
    ai_result: str
    created_at: str


def build_rag_prompt(content: str, knowledge_context: str) -> str:
    """Build the prompt with retrieved knowledge injected as context."""
    return f"""
你是 AI 輔助的軟體工作流程整理助理。
請閱讀會議紀錄或需求內容，並用繁體中文產生以下內容：

1. 會議與需求摘要
2. TODO 清單
3. API 草稿
4. Markdown 知識筆記
5. 使用了哪些相關知識筆記，以及使用原因

請把相關知識筆記當作背景脈絡。若知識筆記與本次內容沒有直接關聯，請簡短說明，
並以會議紀錄或需求內容為主要依據。

相關知識筆記：
{knowledge_context or "沒有找到相關的知識筆記。"}

會議紀錄或需求內容：
{content}
"""


@app.get("/health")
def health_check() -> dict[str, bool | str]:
    """Return basic application health and API-key configuration status."""
    return {
        "status": "ok",
        "openai_configured": is_openai_configured(),
    }


@app.post("/summarize", response_model=SummaryOutput)
def summarize_meeting(data: MeetingInput) -> SummaryOutput:
    """Summarize meeting notes with retrieved knowledge injected into the prompt."""
    client = OpenAI(api_key=get_openai_api_key())
    related_knowledge = search_knowledge(data.content, top_k=2)
    knowledge_context = "\n\n".join(
        f"來源：{item['source']}\n內容：\n{item['content']}"
        for item in related_knowledge
    )
    prompt = build_rag_prompt(data.content, knowledge_context)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    result = response.choices[0].message.content or ""
    save_meeting(data.content, result)
    return SummaryOutput(result=result, related_knowledge=related_knowledge)


@app.get("/history", response_model=list[HistoryItem])
def history() -> list[HistoryItem]:
    """Return saved meeting summary history."""
    return [
        HistoryItem(
            id=row[0],
            content=row[1],
            ai_result=row[2],
            created_at=row[3],
        )
        for row in get_history()
    ]


def main() -> None:
    """Run the application."""
    api_key = get_openai_api_key(required=False)
    status = "已設定" if api_key else "未設定"
    print(f"AI Meeting Copilot - OpenAI API key {status}")


if __name__ == "__main__":
    main()
