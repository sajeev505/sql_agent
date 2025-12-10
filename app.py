from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import logging
from database import list_databases, list_tables, list_columns
from query_generator import generate_sql_query, execute_query

# Initialize FastAPI
app = FastAPI(title="AI Powered SQL Query Generator")

# Logging
logging.basicConfig(level=logging.DEBUG)

# Request Models
class QueryRequest(BaseModel):
    natural_query: str
    database_name: str
    model: str = "gemini-2.5-pro"

class ExecuteRequest(BaseModel):
    sql_query: str

# --- Routes ---

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "🤖 AI Powered SQL Query Generator API",
        "status": "running",
        "endpoints": {
            "GET /databases": "List all databases",
            "GET /tables/{database_name}": "List tables in a database",
            "GET /columns/{database_name}/{table_name}": "List columns in a table",
            "POST /generate_sql": "Generate SQL from natural language",
            "POST /execute_sql": "Execute a SQL query"
        },
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/databases")
def get_databases():
    """Endpoint to list all databases."""
    dbs = list_databases()
    if not dbs:
        raise HTTPException(status_code=500, detail="Failed to fetch databases")
    return {"databases": dbs}

@app.get("/tables/{database_name}")
def get_tables(database_name: str):
    """Endpoint to list tables in a database."""
    tables = list_tables(database_name)
    return {"tables": tables}

@app.get("/columns/{database_name}/{table_name}")
def get_columns(database_name: str, table_name: str):
    """Endpoint to list columns in a table."""
    cols = list_columns(database_name, table_name)
    return {"columns": cols}

@app.post("/generate_sql")
def generate_sql_endpoint(request: QueryRequest):
    """Endpoint to generate SQL from natural language."""
    sql = generate_sql_query(request.natural_query, request.database_name, request.model)
    if "Error" in sql or "Rate limited" in sql:
         raise HTTPException(status_code=400, detail=sql)
    return {"sql_query": sql}

@app.post("/execute_sql")
def execute_sql_endpoint(request: ExecuteRequest):
    """Endpoint to execute a given SQL query."""
    result = execute_query(request.sql_query)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
