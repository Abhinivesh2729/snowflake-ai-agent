
import os
import snowflake.connector
from dotenv import load_dotenv
from sql_gen import generate_sql

load_dotenv()

def ask_agent(question: str):
    sql = generate_sql(question)
    print("\nGenerated SQL:", sql)

    # Basic safety check
    if not sql.upper().startswith("SELECT "):
        raise ValueError("Only SELECT queries are allowed.")

    if ";" in sql or "--" in sql or "/*" in sql:
        raise ValueError("Unsafe SQL rejected.")

    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse="COMPUTE_WH",
        database="AI_LEARNING",
        schema="PUBLIC",
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            print("\nResults:", cursor.fetchall())
    finally:
        conn.close()


if __name__ == "__main__":
    question = input("Ask a question: ")
    ask_agent(question)
