# AI Meeting Copilot

Project scaffold for an AI meeting assistant.

## Run

```powershell
streamlit run ui/streamlit_app.py
```

## Run With Docker

Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

Start the API and Streamlit UI:

```powershell
docker compose up --build
```

Open:

- FastAPI docs: http://localhost:8000/docs
- Streamlit UI: http://localhost:8501
