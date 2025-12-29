import httpx, os, json
from typing import List, Dict

LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1/chat/completions")

async def generate_sql_or_pandas(messages: List[Dict], question: str, tables):
    table_names = []
    for t in tables:
        if isinstance(t, (list, tuple)):
            table_names.append(str(t[0]))
        else:
            table_names.append(str(t))

    system = (
        "You are a data analyst. Available tables: "
        + ", ".join(table_names)
        + ". Prefer SQL unless impossible. "
        "Return strict JSON with keys: language (sql|pandas), code, explanation."
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": system}] + messages + [
            {"role": "user", "content": question}
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(LLM_API_URL, json=payload)
        r.raise_for_status()
        data = r.json()

    content = data["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except Exception:
        return {"language": "pandas", "code": "", "explanation": content}
