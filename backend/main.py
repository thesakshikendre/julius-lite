from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd, uuid
from io import BytesIO
from typing import Dict
from models import AskRequest, UploadResponse, AnalysisResult
from llm_client import generate_sql_or_pandas
from db import SessionDB

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SESSIONS: Dict[str, SessionDB] = {}

@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "CSV only")
    df = pd.read_csv(BytesIO(await file.read()))
    sid = str(uuid.uuid4())

    db = SessionDB()
    table = file.filename.replace(".csv", "")
    db.register_df(table, df)
    SESSIONS[sid] = db

    return UploadResponse(session_id=sid, tables=db.list_tables())

@app.post("/ask", response_model=AnalysisResult)
async def ask(req: AskRequest):
    if req.session_id not in SESSIONS:
        raise HTTPException(404, "Session not found")

    db = SESSIONS[req.session_id]
    llm = await generate_sql_or_pandas(
        [m.dict() for m in req.messages],
        req.question,
        db.list_tables(),
    )

    language = llm.get("language", "sql")
    code = llm.get("code", "").strip()

    if language != "sql" or not code:
        raise HTTPException(400, "Model did not return usable SQL")

    try:
        result = db.sql(code)
    except Exception as e:
        raise HTTPException(400, f"SQL execution failed: {e}")

    return AnalysisResult(
        answer=llm.get("explanation", ""),
        table=result.head(50).to_dict("records"),
        columns=list(result.columns),
        chart=None,
        code=code,
    )
