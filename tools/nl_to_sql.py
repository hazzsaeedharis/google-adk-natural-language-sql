import os
import re
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGPASSWORD = os.getenv("PGPASSWORD", "")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite-001:generateContent"

def ask_llm(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        except (KeyError, IndexError):
            return "Received an unexpected response format from Gemini API."
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

def execute_sql(sql: str) -> dict:
    """Executes a SQL query and returns the results."""
    try:
        conn = psycopg2.connect(
            dbname=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            host=PGHOST,
            port=PGPORT
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        results = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()
        return {"status": "success", "sql": sql, "results": results}
    except Exception as e:
        return {"status": "error", "sql": sql, "error_message": str(e)}

# Table schema context for Gemini prompt
table_schema = """
Tables and columns:
- distribution(name, display_name, latitude, longitude, variable_cost, daily_max_capacity, schedule_time)
- sort(name, display_name, latitude, longitude, variable_cost, daily_max_capacity, schedule_time)
- stores(name, display_name, latitude, longitude, variable_cost, daily_max_capacity, schedule_time)
"""

def extract_sql(raw_sql: str) -> str:
    # Remove markdown code block markers if present
    cleaned = re.sub(r"^```sql|^```|```$", "", raw_sql, flags=re.MULTILINE).strip()
    # Find the first SELECT ... ; block (non-greedy, multiline)
    match = re.search(r"(SELECT[\s\S]+?;)", cleaned, re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        sql = cleaned
    # Collapse all whitespace (including newlines) to a single space
    sql_single_line = re.sub(r"\s+", " ", sql)
    return sql_single_line

def nl_to_sql_and_execute(question: str) -> dict:
    """Converts a natural language question to SQL using Gemini, executes it, and returns the results."""
    prompt = f"""
You are an expert SQL generator. Given a question and the following table schema, write a safe SQL SELECT query (PostgreSQL dialect) that answers the question. Only use the tables and columns provided. Do not use DROP, DELETE, UPDATE, or INSERT. Only generate the SQL query, nothing else.

Schema:
{table_schema}

Question: {question}
SQL:
"""
    raw_sql = ask_llm(prompt)
    print("raw_sql: ", raw_sql)
    sql = extract_sql(raw_sql)
    print("sql: ", sql)
    return execute_sql(sql)
