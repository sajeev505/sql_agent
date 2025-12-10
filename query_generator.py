import os
import re
import json
import time
import google.generativeai as genai
import openai
import sqlparse
from dotenv import load_dotenv
from sqlalchemy import text
from database import engine, list_tables, list_columns

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rate limiting configuration
last_api_call_time = 0
RATE_LIMIT_SECONDS = 60

def clean_sql_query(response_text):
    """Removes markdown and cleans the SQL query."""
    # Remove markdown code blocks (```sql ... ```)
    clean_query = re.sub(r'```sql|```', '', response_text).strip()
    return clean_query

def fetch_limited_schema(database_name, max_tables=5, max_columns=5):
    """
    Fetches a limited schema to avoid hitting API token limits.
    """
    schema_summary = {}
    tables = list_tables(database_name)[:max_tables]
    
    for table in tables:
        columns = list_columns(database_name, table)[:max_columns]
        schema_summary[table] = [col['Field'] for col in columns]
        
    return schema_summary

def generate_sql_query(natural_query, database_name, model="gemini-2.5-pro"):
    """
    Generates an SQL query from natural language using Google Gemini or OpenAI.
    Rate limited to 1 call per 60 seconds.
    """
    global last_api_call_time
    
    # Rate limiting check
    current_time = time.time()
    elapsed = current_time - last_api_call_time
    if last_api_call_time > 0 and elapsed < RATE_LIMIT_SECONDS:
        wait_time = int(RATE_LIMIT_SECONDS - elapsed)
        return f"Rate limited. Please wait {wait_time} seconds before making another request."
    
    schema = fetch_limited_schema(database_name)
    
    prompt = f"""
    You are an expert SQL Assistant. 
    Convert the following natural language query into a valid SQL query for MySQL.
    
    Database Schema:
    {json.dumps(schema, indent=2)}
    
    Query: "{natural_query}"
    
    Target Database: {database_name}
    
    Return ONLY the SQL query. Do not include explanations or markdown.
    """
    
    try:
        if model.startswith("gpt"):
            # Use OpenAI
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful SQL assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            sql_query = response.choices[0].message.content
        else:
            # Use Gemini
            gen_model = genai.GenerativeModel(model)
            response = gen_model.generate_content(prompt)
            sql_query = response.text
        
        # Update last API call time after successful call
        last_api_call_time = time.time()
        
        return clean_sql_query(sql_query)
        
    except Exception as e:
        return f"Error generating SQL: {str(e)}"

def execute_query(sql_query):
    """
    Executes the SQL query and returns the results.
    """
    try:
        # Validate syntax
        parsed = sqlparse.parse(sql_query)
        if not parsed:
            return {"error": "Invalid SQL syntax"}

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            # Convert result to list of dicts
            rows = result.fetchall()
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
            
            return {"data": data, "columns": list(columns)}
            
    except Exception as e:
        return {"error": str(e)}
