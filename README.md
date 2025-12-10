# AI Powered SQL Query Generator

An intelligent application that converts natural language questions into SQL queries using Google's Gemini AI, with a FastAPI backend and Streamlit frontend.

## 🚀 Features

- **Natural Language to SQL**: Convert plain English questions into valid MySQL queries
- **Database Explorer**: Browse databases, tables, and columns through an intuitive sidebar
- **Query Execution**: Execute generated SQL queries and view results in a data table
- **Schema-Aware Generation**: AI uses your actual database schema for accurate query generation

## 📁 Project Structure

```
SQL_agent/
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (credentials)
├── database.py           # Database connection & schema retrieval
├── query_generator.py    # Gemini AI integration & SQL generation
├── app.py                # FastAPI backend (REST API)
├── ui.py                 # Streamlit frontend (UI)
└── README.md             # This file
```

## 🛠️ Prerequisites

- Python 3.8+
- MySQL Server running locally
- Gemini API Key (get from [AI Studio](https://aistudio.google.com/apikey))

## 📦 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   
   Edit the `.env` file with your actual credentials:
   ```env
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=your_database
   MYSQL_PORT=3306
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

## ▶️ How to Run

1. **Start MySQL** and ensure your database is running.

2. **Start the Backend (FastAPI):**
   ```bash
   uvicorn app:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

3. **Start the Frontend (Streamlit)** in a new terminal:
   ```bash
   streamlit run ui.py
   ```
   The UI will open in your browser at `http://localhost:8501`

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/databases` | GET | List all databases |
| `/tables/{database_name}` | GET | List tables in a database |
| `/columns/{database_name}/{table_name}` | GET | List columns in a table |
| `/generate_sql` | POST | Generate SQL from natural language |
| `/execute_sql` | POST | Execute a SQL query |

## 📝 Usage

1. Click "List Databases" in the sidebar to see available databases
2. Select a database from the dropdown
3. Explore tables and columns using the sidebar buttons
4. Type your question in plain English (e.g., "Show all customers from New York")
5. Click "Generate SQL" to create the query
6. Review the generated SQL and click "Execute SQL" to run it
7. View the results in the data table

## ⚠️ Important Notes

- Ensure your MySQL server is running before starting the application
- Keep your Gemini API key secure and never commit it to version control
- The application uses Gemini 2.5 Pro for high-quality SQL generation

## 📄 License

MIT License
