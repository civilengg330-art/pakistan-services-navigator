import os
import json
import re
import streamlit as st
from groq import Groq

DEFAULT_MODEL = "openai/gpt-oss-120b"

def get_groq_client():
    """
    Retrieves the Groq API Key from Streamlit secrets or system environment variables.
    Returns an initialized Groq client.
    """
    api_key = None
    
    # Check Streamlit secrets first (for cloud deployment)
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
        
    # Fallback to os.environ
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured in Streamlit Secrets or Environment Variables.")
        
    return Groq(api_key=api_key)

def clean_and_parse_json(text_response: str) -> dict:
    """
    Cleans raw LLM response text, strips markdown code blocks,
    and parses it into a valid Python dictionary.
    """
    cleaned = text_response.strip()
    # Strip markdown ```json ... ``` wrapper if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    
    try:
        return json.loads(cleaned.strip())
    except json.JSONDecodeError as e:
        # Fallback: attempt to find first '{' and last '}'
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(cleaned[start:end+1])
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nRaw output: {text_response}")
