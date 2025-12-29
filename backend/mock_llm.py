# MOCK LLM - Returns working SQL instantly (no Ollama needed)
async def generate_sql_or_pandas(messages, question, tables):
    if not tables:
        return {
            "language": "sql",
            "code": "SELECT 'No tables loaded' as message",
            "explanation": "Upload a CSV first!"
        }
    
    table = tables[0]
    
    # Smart SQL based on question keywords
    question_lower = question.lower()
    if "top" in question_lower or "highest" in question_lower:
        return {
            "language": "sql",
            "code": f"SELECT * FROM {table} ORDER BY 1 DESC LIMIT 5",
            "explanation": f"Top 5 rows from {table} (sorted by first column)"
        }
    elif "count" in question_lower:
        return {
            "language": "sql", 
            "code": f"SELECT COUNT(*) as total_rows FROM {table}",
            "explanation": f"Row count from {table}"
        }
    elif "average" in question_lower or "avg" in question_lower:
        return {
            "language": "sql",
            "code": f"SELECT AVG(*) FROM {table} LIMIT 1",
            "explanation": f"Average values from {table}"
        }
    else:
        return {
            "language": "sql",
            "code": f"SELECT * FROM {table} LIMIT 10",
            "explanation": f"Preview of {table} (first 10 rows)"
        }
