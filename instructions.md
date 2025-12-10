# 🚀 Setup Instructions

Follow these steps after the application files have been created.

---

## Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This installs all required packages including FastAPI, Streamlit, OpenAI, SQLAlchemy, etc.

---

## Step 2: Set Up MySQL Database

Ensure MySQL is installed and running on your machine.

**Option A: Using MySQL Workbench**
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Create a test database if you don't have one:
   ```sql
   CREATE DATABASE test_db;
   ```

**Option B: Using Command Line**
```bash
mysql -u root -p
CREATE DATABASE test_db;
```

---

## Step 3: Configure Environment Variables

Open the `.env` file in your project directory and update the following values:

```env
# Database Credentials
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD    # ← Replace with your MySQL password
MYSQL_DATABASE=test_db                 # ← Replace with your database name
MYSQL_PORT=3306

# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx  # ← Replace with your actual API key
```

---

## Step 4: Get Your OpenAI API Key

1. Go to **https://platform.openai.com/api-keys**
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Copy the key (it starts with `sk-proj-...` or `sk-...`)
5. Paste it in the `.env` file as the value for `OPENAI_API_KEY`

> ⚠️ **Important**: Never share your API key publicly or commit it to version control!

---

## Step 5: Start the Backend Server

Open **Terminal 1** and run:

```bash
uvicorn app:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

Keep this terminal running!

---

## Step 6: Start the Frontend UI

Open **Terminal 2** (keep the first one running) and run:

```bash
streamlit run ui.py
```

Your browser will automatically open to `http://localhost:8501`

---

## Step 7: Using the Application

1. **List Databases**: Click the button in the sidebar to see all MySQL databases
2. **Select Database**: Choose your target database from the dropdown
3. **Explore Tables**: Click "Show Tables" to see available tables
4. **View Columns**: Select a table and click "Show Columns" to see its structure
5. **Ask Questions**: Type natural language questions like:
   - "Show all records from the users table"
   - "Find customers who signed up last month"
   - "Count the total orders by product category"
6. **Generate SQL**: Click the button to convert your question to SQL
7. **Execute**: Review the SQL and click "Execute SQL" to run it

---

## 🔧 Troubleshooting

### "Connection Error" in the UI
- Make sure the FastAPI backend is running on port 8000
- Check that MySQL is running

### "Failed to fetch databases"
- Verify your MySQL credentials in `.env`
- Ensure MySQL service is started

### OpenAI API Errors
- Check that your API key is valid and has available credits
- Ensure the key is correctly pasted without extra spaces

### Import Errors
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8 or higher

---

## 📁 File Locations Reference

| File | Purpose |
|------|---------|
| `.env` | **← PUT YOUR API KEY HERE** |
| `requirements.txt` | Python dependencies |
| `database.py` | Database connection logic |
| `query_generator.py` | OpenAI integration |
| `app.py` | FastAPI backend |
| `ui.py` | Streamlit frontend |

---

## 💡 Tips

- Use **GPT-3.5-Turbo** instead of GPT-4 for faster, cheaper queries (edit `query_generator.py`, line ~51)
- Add more tables to your database for better testing
- The schema fetcher limits to 5 tables/columns by default to avoid token limits
