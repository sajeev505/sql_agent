import streamlit as st
import requests
import pandas as pd

# API Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="SQL Query Generator", layout="wide")
st.title("🤖 AI Powered SQL Query Generator")

# --- Sidebar: Database Explorer ---
st.sidebar.header("Database Selection")

# 1. List Databases
if st.sidebar.button("List Databases"):
    try:
        response = requests.get(f"{API_URL}/databases")
        if response.status_code == 200:
            dbs = response.json().get("databases", [])
            st.session_state["databases"] = dbs
            st.sidebar.success("Databases fetched!")
        else:
            st.sidebar.error("Failed to fetch databases")
    except Exception as e:
        st.sidebar.error(f"Connection Error: {e}")

# Database Selectbox
selected_db = st.sidebar.selectbox(
    "Select Database", 
    st.session_state.get("databases", [])
)

# 2. Show Tables
if selected_db:
    if st.sidebar.button("Show Tables"):
        try:
            response = requests.get(f"{API_URL}/tables/{selected_db}")
            if response.status_code == 200:
                tables = response.json().get("tables", [])
                st.session_state["tables"] = tables
                st.sidebar.success(f"Tables in {selected_db} fetched!")
            else:
                st.sidebar.error("Failed to fetch tables")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# Table Selectbox
selected_table = st.sidebar.selectbox(
    "Select Table", 
    st.session_state.get("tables", [])
)

# 3. Show Columns
if selected_table and selected_db:
    if st.sidebar.button("Show Columns"):
        try:
            response = requests.get(f"{API_URL}/columns/{selected_db}/{selected_table}")
            if response.status_code == 200:
                columns = response.json().get("columns", [])
                st.sidebar.write("### Columns:")
                st.sidebar.table(columns)
            else:
                st.sidebar.error("Failed to fetch columns")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# --- Main Area: Query Generator ---

st.subheader("Generate SQL Query")

# User Input
natural_query = st.text_area("Enter your question in plain English:", height=100)

if st.button("Generate SQL"):
    if natural_query and selected_db:
        payload = {"natural_query": natural_query, "database_name": selected_db}
        try:
            response = requests.post(f"{API_URL}/generate_sql", json=payload)
            if response.status_code == 200:
                generated_sql = response.json().get("sql_query")
                st.session_state["generated_sql"] = generated_sql
                st.success("SQL Query Generated!")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
    else:
        st.warning("Please select a database and enter a query.")

# Display Generated SQL
if "generated_sql" in st.session_state:
    sql_query = st.code(st.session_state["generated_sql"], language="sql")
    
    # Execute SQL
    if st.button("Execute SQL"):
        try:
            payload = {"sql_query": st.session_state["generated_sql"]}
            response = requests.post(f"{API_URL}/execute_sql", json=payload)
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    st.write("### Query Results:")
                    st.dataframe(pd.DataFrame(data))
                else:
                    st.info("Query executed successfully, but returned no results.")
            else:
                st.error(f"Execution Error: {response.text}")
        except Exception as e:
            st.error(f"Error executing query: {e}")
