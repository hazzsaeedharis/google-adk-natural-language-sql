# ADK NL2SQL Agent

This project provides an agent, built using Google ADK, that converts natural language questions into SQL queries for a PostgreSQL database and returns the results. It uses Google's Gemini API for natural language processing and supports querying tables such as 'distribution', 'sort', and 'stores' (as in the example 'optimusx' database). You can modify the schema in the code to match your own database tables and columns.

## Features
- Converts natural language to SQL (PostgreSQL dialect)
- Executes queries safely (SELECT only)
- Returns results as JSON
- Built with [google-adk](https://pypi.org/project/google-adk/)

## Setup
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your database and API credentials.

## Environment Variables
- `PGDATABASE`: Name of your Postgres database (e.g., optimusx)
- `PGUSER`: Postgres username
- `PGHOST`: Postgres host
- `PGPORT`: Postgres port
- `PGPASSWORD`: Postgres password
- `GOOGLE_API_KEY`: Gemini API key

## Usage
Import and use the agent in your Python code, or extend as needed. To use with your own database, update the table schema in `multi_tool_agent/agent.py`.

---
**Note:** This project is for demonstration purposes. Do not use in production without proper security review. 