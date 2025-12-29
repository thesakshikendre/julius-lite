Julius Lite – AI Data Analyst (SQL-first)
A Julius.ai–style AI data analyst which allows upload of CSV files and asking
The user's queries in natural language, the system gives SQL using an LLM.

then executes it locally with DuckDB, returning the results plus reproducible code.
Features
- Upload CSV files
- Engage in conversation with your data using natural language
- LLM-generated SQL (DuckDB)
- Multi-table joins
- UI display of reproducible SQL

Frontend created in: - React + Vite
FastAPI backend
Tech Stack

-Backend: FastAPI, DuckDB, Pandas

- Frontend: React, TypeScript, Vite
- API LY Account: OpenAI / Ollama / Gemini Compatible
## Running Locally
backend
```bash
cd backend
python -m venv venv source venv/bin/activate   # Windows: venv\\Scripts\\activate pip install -r requirements.txt uvicorn main:app --reload --port 8000