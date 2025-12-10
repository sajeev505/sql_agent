import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database Credentials
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE") # Default DB, can be changed dynamically

# Create Database Connection URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        connection = engine.connect()
        logging.debug(f"Connected to MySQL at {DB_HOST}")
        return connection
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise e

def list_databases():
    """Lists all available databases in the MySQL server."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result]
            return databases
    except Exception as e:
        logging.error(f"Error listing databases: {e}")
        return []

def list_tables(database_name):
    """Lists all tables in a specific database."""
    try:
        with engine.connect() as connection:
            # Switch to the selected database could be done in query or by engine URL update
            # Here we just query specific DB
            result = connection.execute(text(f"SHOW TABLES FROM {database_name}"))
            tables = [row[0] for row in result]
            return tables
    except Exception as e:
        logging.error(f"Error listing tables for {database_name}: {e}")
        return []

def list_columns(database_name, table_name):
    """Lists all columns for a specific table in a database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SHOW COLUMNS FROM {database_name}.{table_name}"))
            # returning a list of dictionaries for better detail (Field, Type, etc.)
            columns = [{"Field": row[0], "Type": row[1]} for row in result]
            return columns
    except Exception as e:
        logging.error(f"Error listing columns for {table_name}: {e}")
        return []
