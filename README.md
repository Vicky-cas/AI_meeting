# AI-powered workflow assistant for:

- meeting summarization
- requirement extraction
- API draft generation
- lightweight RAG knowledge retrieval
- AI-assisted software collaboration

This project is designed to simulate a lightweight enterprise AI workflow assistant instead of a simple chatbot demo.

---

# Features

## AI Workflow Features

- Meeting / requirement summarization
- TODO extraction
- API draft generation
- Markdown knowledge note generation
- Lightweight RAG knowledge retrieval

## Engineering Features

- FastAPI backend
- Streamlit UI
- Dockerized deployment
- REST API architecture
- AI-assisted workflow automation

---

# Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | OpenAI API |
| Vector Search | FAISS |
| Embedding Model | sentence-transformers |
| Database | SQLite |
| Deployment | Docker |
| Version Control | Git |

---

# Project Structure

```txt
AI_meeting/
│
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── prompts.py
│   ├── utils.py
│
├── ui/
│   └── streamlit_app.py
│
├── data/
│   └── knowledge/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
````

---

# Workflow

```txt
User Meeting Input
        ↓
FastAPI Backend
        ↓
OpenAI API
        ↓
AI Processing
 ├─ Requirement Summary
 ├─ TODO Extraction
 ├─ API Draft
 └─ Knowledge Note
        ↓
RAG Knowledge Retrieval
```

---

# Run Locally

## 1. Clone Repository

```bash
git clone https://github.com/Vicky-cas/AI_meeting.git
cd AI_meeting
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create .env File

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 5. Run FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000/docs
```

---

## 6. Run Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

Open:

```txt
http://localhost:8501
```

---

# Run With Docker

## Start Services

```bash
docker compose up --build
```

---

## Open

### FastAPI Docs

```txt
http://localhost:8000/docs
```

### Streamlit UI

```txt
http://localhost:8501
```

---

# Why This Project

This project explores how AI workflows can support software collaboration and requirement management processes.

Instead of building a simple chatbot demo, the goal is to simulate a lightweight enterprise AI workflow assistant that can:

* translate business discussions into actionable tasks
* organize knowledge into reusable documentation
* support AI-assisted software development workflows
* improve workflow efficiency through AI automation

---

# Disclaimer

All knowledge base content inside the project is mock/demo data only.

No real company data or confidential business information is included.

```
```
