import httpx, os, json
from typing import List, Dict

# MOCK MODE - Works instantly!
from mock_llm import generate_sql_or_pandas

async def generate_sql_or_pandas(messages: List[Dict], question: str, tables):
    # return await real_llm_call(...)  # Real LLM later
    return await generate_sql_or_pandas(messages, question, tables)





