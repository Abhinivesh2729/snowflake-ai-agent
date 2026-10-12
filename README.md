# Snowflake AI Agent

A small proof of concept that turns a plain-English question into a Snowflake SQL query, runs it and prints the results.

## How it works

1. **`sql_gen.py`** sends your question and the table schema to a local LLM (`qwen2.5:3b` through [Ollama](https://ollama.com)). The model returns a single `SELECT` query against `AI_LEARNING.PUBLIC.CUSTOMERS`.
2. **`agent.py`** checks the generated SQL before running it:
   - It must start with `SELECT`.
   - It must not contain `;`, `--` or `/*`.

   If the query passes, `agent.py` runs it on Snowflake (warehouse `COMPUTE_WH`, database `AI_LEARNING`, schema `PUBLIC`) and prints the rows.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install snowflake-connector-python python-dotenv ollama
ollama pull qwen2.5:3b
```

Create a `.env` file in the project root:

```env
SNOWFLAKE_ACCOUNT=xy12345.ap-south-1
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
```

## Run

```bash
python agent.py
```

Example session:

```
Ask a question: Total purchase amount by city

Generated SQL: SELECT CITY, SUM(PURCHASE_AMOUNT) FROM AI_LEARNING.PUBLIC.CUSTOMERS GROUP BY CITY

Results: [('Chennai', 12500), ('Bangalore', 9800)]
```

## Expected table

```sql
CREATE TABLE AI_LEARNING.PUBLIC.CUSTOMERS (
  ID INTEGER,
  NAME STRING,
  CITY STRING,
  PURCHASE_AMOUNT NUMBER
);
```
