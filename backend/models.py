from pydantic import BaseModel
from typing import List, Optional, Any, Dict

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

class ChartSpec(BaseModel):
    type: str
    x: List[Any]
    y: List[float]
    title: str

class AnalysisResult(BaseModel):
    answer: str
    table: Optional[List[Dict[str, Any]]]
    columns: Optional[List[str]]
    chart: Optional[ChartSpec]
    code: str
