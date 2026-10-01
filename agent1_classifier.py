import json
from categories import CATEGORIES
from llm_client import get_groq_client, DEFAULT_MODEL, clean_and_parse_json
from prompts import AGENT1_SYSTEM_PROMPT

def classify_query(user_query: str) -> dict:
    """
    Uses Groq LLM to semantically classify user query into 16 categories/subcategories.
    Returns a dictionary with status, category, service, and clarification_question.
    """
    client = get_groq_client()
    taxonomy_json = json.dumps(CATEGORIES, indent=2)
    
    system_prompt = AGENT1_SYSTEM_PROMPT.format(taxonomy_json=taxonomy_json)
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User Query: '{user_query}'"}
        ],
        temperature=0.1
    )
    
    raw_content = response.choices[0].message.content
    parsed = clean_and_parse_json(raw_content)
    return parsed
