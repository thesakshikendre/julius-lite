from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import pandas as pd
import uuid
from io import BytesIO
import duckdb

app = FastAPI(title="Julius Lite AI")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Inline models
class ChatMessage(BaseModel):
    role: str
    content: str

class AskRequest(BaseModel):
    question: str
    messages: List[ChatMessage]
    model: str
    session_id: str

class UploadResponse(BaseModel):
    session_id: str
    tables: List[str]

class AnalysisResult(BaseModel):
    answer: str
    table: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    code: str

# Inline DuckDB
class SessionDB:
    def __init__(self):
        self.con = duckdb.connect(database=':memory:')
    
    def register_df(self, name: str, df: pd.DataFrame):
        self.con.register(name, df)
    
    def list_tables(self):
        return [r[0] for r in self.con.execute("SHOW TABLES").fetchall()]
    
    def sql(self, query: str) -> pd.DataFrame:
        return self.con.execute(query).df()

# MOCK LLM (your mock_llm.py logic inline)
async def generate_sql_or_pandas(question: str, tables: List[str]):
    if not tables:
        return {
            "language": "sql", 
            "code": "SELECT 'Upload CSV first!' as message",
            "explanation": "Please upload a CSV file first"
        }
    
    table = tables[0]
    q = question.lower()
    
    if "top" in q or "highest" in q:
        return {
            "language": "sql",
            "code": f"SELECT * FROM {table} ORDER BY 1 DESC LIMIT 5",
            "explanation": f"Top 5 rows from {table}"
        }
    elif "count" in q or "total" in q:
        return {
            "language": "sql",
            "code": f"SELECT COUNT(*) as total_rows FROM {table}",
            "explanation": f"Total row count from {table}"
        }
    elif "avg" in q or "average" in q:
        return {
            "language": "sql",
            "code": f"SELECT AVG(*) FROM {table} LIMIT 1",
            "explanation": f"Average values from {table}"
        }
    else:
        return {
            "language": "sql",
            "code": f"SELECT * FROM {table} LIMIT 10",
            "explanation": f"Preview of first 10 rows from {table}"
        }

SESSIONS: Dict[str, SessionDB] = {}

@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files allowed")
    
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    
    sid = str(uuid.uuid4())
    db = SessionDB()
    table = file.filename.replace(".csv", "").replace(" ", "_").replace("-", "_")
    
    if len(table) > 20:  # DuckDB table name limit
        table = "data_table"
    
    db.register_df(table, df)
    SESSIONS[sid] = db
    
    return UploadResponse(
        session_id=sid, 
        tables=db.list_tables()
    )

@app.post("/ask", response_model=AnalysisResult)
async def ask(req: AskRequest):
    if req.session_id not in SESSIONS:
        raise HTTPException(404, "Session expired. Upload CSV again.")
    
    db = SESSIONS[req.session_id]
    llm = await generate_sql_or_pandas(req.question, db.list_tables())
    
    language = llm.get("language", "sql")
    code = llm.get("code", "").strip()
    
    if language != "sql" or not code:
        raise HTTPException(400, "Could not generate SQL")
    
    try:
        result = db.sql(code)
        return AnalysisResult(
            answer=llm["explanation"],
            table=result.head(20).to_dict("records"),
            columns=list(result.columns),
            code=code
        )
    except Exception as e:
        raise HTTPException(400, f"SQL Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "Julius Lite Backend ✅ 100% Working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

