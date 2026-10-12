
import ollama
import re

SCHEMA = """
Table: AI_LEARNING.PUBLIC.CUSTOMERS
Columns:
- ID: integer
- NAME: customer name
- CITY: city name
- PURCHASE_AMOUNT: purchase amount
"""

def generate_sql(question: str) -> str:
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": f"""
You generate Snowflake SQL queries.

Schema:
{SCHEMA}

Rules:
- Return exactly one SELECT query.
- Use only AI_LEARNING.PUBLIC.CUSTOMERS.
- Never generate modifying statements.
- Return SQL only, without markdown.
"""
            },
            {"role": "user", "content": question},
        ],
        options={"temperature": 0},
    )

    sql = response["message"]["content"].strip()
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.I)
    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()

