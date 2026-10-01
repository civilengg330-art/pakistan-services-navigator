import json
from llm_client import get_groq_client, DEFAULT_MODEL, clean_and_parse_json
from prompts import AGENT4_SYSTEM_PROMPT

def generate_final_response(user_query: str, agent3_output: dict) -> dict:
    """
    Converts Agent 3 research into structured dictionary payload for custom Streamlit rendering.
    """
    client = get_groq_client()
    
    input_payload = f"""
    Original User Query: {user_query}
    Gathered Research:
    {json.dumps(agent3_output, indent=2)}
    """
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": AGENT4_SYSTEM_PROMPT},
            {"role": "user", "content": input_payload}
        ],
        temperature=0.2
    )
    
    raw_content = response.choices[0].message.content
    return clean_and_parse_json(raw_content)
