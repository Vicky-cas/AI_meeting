"""FastAPI entry point for AI Meeting Copilot."""

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel, Field

from app.config import get_openai_api_key, is_openai_configured
from app.rag import search_knowledge


app = FastAPI(title="AI Meeting Copilot")


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


def build_rag_prompt(content: str, knowledge_context: str) -> str:
    """Build the prompt with retrieved knowledge injected as context."""
    return f"""
You are an AI software workflow assistant.
Please read the meeting notes and generate the following:

1. Meeting summary
2. TODO list
3. API draft
4. Markdown knowledge note
5. Which related knowledge notes were used and why

Use the related knowledge notes as background context. If they are not directly
relevant, say so briefly and keep the answer grounded in the meeting notes.

Related knowledge notes:
{knowledge_context or "No related knowledge notes were found."}

Meeting notes:
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
        f"Source: {item['source']}\nContent:\n{item['content']}"
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
    return SummaryOutput(result=result, related_knowledge=related_knowledge)


def main() -> None:
    """Run the application."""
    api_key = get_openai_api_key(required=False)
    status = "configured" if api_key else "missing"
    print(f"AI Meeting Copilot - OpenAI API key is {status}")


if __name__ == "__main__":
    main()
