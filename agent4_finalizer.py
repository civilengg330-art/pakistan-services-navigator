import json
from llm_client import get_groq_client, DEFAULT_MODEL
from prompts import AGENT4_SYSTEM_PROMPT

def generate_final_response(user_query: str, agent3_output: dict) -> str:
    """
    Converts Agent 3 research into a clear, citizen-friendly markdown answer.
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
        temperature=0.3
    )
    
    return response.choices[0].message.content
