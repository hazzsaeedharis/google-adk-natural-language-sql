from google.adk.agents import Agent
from tools.nl_to_sql import nl_to_sql_and_execute

root_agent = Agent(
    name="NL2SQL_Agent",
    model="gemini-2.0-flash",
    description=(
        "Agent that converts natural language questions to SQL queries for the 'optimusx' Postgres database and returns the results."
    ),
    instruction=(
        "You are a helpful agent that takes user questions about the 'distribution', 'sort', and 'stores' tables, generates SQL, executes it, and returns the results."
    ),
    tools=[nl_to_sql_and_execute],
)
