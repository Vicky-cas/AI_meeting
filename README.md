# AI Meeting Assistance

這是一個輕量級的企業 AI 工作流程助理，用來把會議紀錄、需求訪談、Bug 回報或 API 需求整理成可執行的軟體開發輸出。

這個專案不是單純的聊天機器人範例，而是模擬實務中常見的 AI 輔助協作流程：輸入非結構化內容，透過 LLM 與 RAG 知識檢索，產出摘要、TODO、API 草稿與可重複使用的知識筆記。

---

## 功能特色

### AI 工作流程

- 會議與需求內容摘要
- TODO 與後續行動項目萃取
- API 草稿產生
- Markdown 知識筆記產生
- 輕量級 RAG 知識庫檢索
- 分析紀錄保存與查詢

### 工程功能

- FastAPI 後端服務
- Streamlit 前端介面
- SQLite 本機資料庫
- FAISS 向量檢索
- Docker / Docker Compose 部署
- GitHub Actions CI
- REST API 架構

---

## 技術架構

| 類別 | 技術 |
|---|---|
| 後端 | FastAPI |
| 前端 | Streamlit |
| LLM | OpenAI API |
| 向量檢索 | FAISS |
| Embedding Model | sentence-transformers |
| 資料庫 | SQLite |
| 部署 | Docker |
| CI | GitHub Actions |
| 版本控制 | Git |

---

## 專案結構

```txt
AI_meeting/
+-- app/
|   +-- main.py          # FastAPI 入口與 API 路由
|   +-- db.py            # SQLite 存取邏輯
|   +-- config.py        # 環境變數與設定
|   +-- rag.py           # RAG 知識檢索
|   +-- prompts.py       # Prompt 管理
|   +-- utils.py         # 共用工具
+-- ui/
|   +-- streamlit_app.py # Streamlit 前端介面
+-- data/
|   +-- knowledge/       # Markdown 知識庫資料
+-- database/
|   +-- app.db           # SQLite 資料庫
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- README.md
```

---

## 工作流程

```txt
使用者輸入會議紀錄 / 需求 / Bug 回報
        |
        v
FastAPI 後端接收請求
        |
        v
RAG 檢索 data/knowledge 相關知識
        |
        v
OpenAI API 進行內容整理與生成
        |
        v
輸出：
- 會議 / 需求摘要
- TODO 清單
- API 草稿
- Markdown 知識筆記
- 使用到的相關知識來源
        |
        v
SQLite 保存分析紀錄
```

---

## API 端點

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/health` | 檢查服務狀態與 OpenAI API Key 是否已設定 |
| POST | `/summarize` | 分析輸入內容並回傳 AI 結構化結果 |
| GET | `/history` | 取得最近的分析紀錄 |

---

## 本機執行

### 1. 複製專案

```bash
git clone https://github.com/Vicky-cas/AI_meeting.git
cd AI_meeting
```

### 2. 建立虛擬環境

Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Mac / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝套件

```bash
pip install -r requirements.txt
```

### 4. 建立 `.env` 檔案

在專案根目錄建立 `.env`：

```env
OPENAI_API_KEY=your_api_key_here
```

### 5. 預先下載 RAG Embedding 模型

`/summarize` API 會使用 Hugging Face 的 `sentence-transformers` 模型進行知識檢索。建議第一次執行前先下載，避免第一次分析時因網路或模型下載造成等待。

Windows:

```powershell
.\venv\Scripts\python.exe -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('model downloaded')"
```

確認本機快取可用：

```powershell
.\venv\Scripts\python.exe -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True); print('local model ok')"
```

Mac / Linux:

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('model downloaded')"
```

確認本機快取可用：

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True); print('local model ok')"
```

### 6. 啟動 FastAPI

```bash
uvicorn app.main:app --reload
```

開啟 API 文件：

```txt
http://127.0.0.1:8000/docs
```

### 7. 啟動 Streamlit UI

另開一個終端機執行：

```bash
streamlit run ui/streamlit_app.py
```

開啟前端介面：

```txt
http://localhost:8501
```

---

## 使用 Docker 執行

啟動服務：

```bash
docker compose up --build
```

服務網址：

```txt
FastAPI Docs: http://localhost:8000/docs
Streamlit UI: http://localhost:8501
```

---

## 知識庫資料

RAG 使用的知識庫位於：

```txt
data/knowledge/
```

可以將公司流程、需求規格、訪談紀錄、資料字典或常見問題整理成 Markdown 檔案放入此資料夾，系統會在分析時檢索相關內容作為背景知識。
此階段尚未將每次輸出的知識筆記納入檢索範圍，下個階段設計是將長期知識與歷史紀錄分層管理，RAG 負責穩定知識檢索，資料庫負責會議歷史保存，查詢時再動態取出相關歷史作為 context。

目前專案內的知識庫資料皆為範例與模擬資料，不包含真實公司機密資訊。

---

## CI

本專案包含 GitHub Actions 設定檔：

```txt
.github/workflows/ci.yml
```

CI 會在 push 到 `main` / `master` 或建立 pull request 時執行，主要檢查：

- 安裝 `requirements.txt` 內的 Python 依賴
- 檢查 `app` 與 `ui` 的 Python 語法
- 確認 Docker image 可以成功建置

---

## 專案目標

這個專案用來展示 AI 如何支援軟體開發協作與需求管理流程，例如：

- 將商務討論轉換成可執行任務
- 將散落的知識整理成可重複使用的文件
- 協助 PM、工程師與業務更快對齊需求
- 透過 AI 自動化減少人工整理會議紀錄的時間

---

## 注意事項

- 專案中的知識庫內容皆為 demo / mock data。
- 使用 OpenAI API 前，請確認 `.env` 已正確設定 `OPENAI_API_KEY`。
