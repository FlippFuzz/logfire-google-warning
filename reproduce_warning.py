"""Minimal reproduction script demonstrating the google-genai / logfire non-text warning.

Requirements:
    pip install -r requirements.txt

Usage:
    # Windows (PowerShell)
    $env:GEMINI_API_KEY="your-api-key"
    python reproduce_warning.py

    # Windows (CMD)
    set "GEMINI_API_KEY=your-api-key"
    python reproduce_warning.py
"""

import os

import logfire
from google import genai
from google.genai import types
from pydantic import BaseModel


# 1. Define a structured output schema
class StructuredOutput(BaseModel):
    summary: str
    status: str


# 2. Define the tool
lookup_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="lookup_data",
            description="Looks up external information for a given query.",
            parameters_json_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."},
                },
                "required": ["query"],
            },
        )
    ]
)

# 3. Configure Logfire instrumentation
logfire.configure(send_to_logfire=False)
logfire.instrument_google_genai()


# 4. Send request to Google GenAI
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
)

config = types.GenerateContentConfig(
    tools=[lookup_tool],
    response_mime_type="application/json",
    response_schema=StructuredOutput,
)

print("--- Calling client.models.generate_content(...) ---")

# Prompt the model to produce a tool call on Turn 1
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Use the lookup_data tool to look up 'test-query'.",
    config=config,
)

print("--- generate_content returned successfully ---")
print("(Notice: user code has not accessed response or response.text at all)")
