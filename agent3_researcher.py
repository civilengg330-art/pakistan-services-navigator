import json
from llm_client import get_groq_client, DEFAULT_MODEL, clean_and_parse_json
from prompts import AGENT3_SYSTEM_PROMPT

def gather_information(user_query: str, category: str, service: str, agent2_output: dict) -> dict:
    """
    Gathers structured information based on the selected web sources and snippets.
    """
    client = get_groq_client()
    
    research_context = f"""
    User Query: {user_query}
    Category: {category}
    Service: {service}
    Selected Sources & Raw Snippets:
    {json.dumps(agent2_output, indent=2)}
    """
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": AGENT3_SYSTEM_PROMPT},
            {"role": "user", "content": research_context}
        ],
        temperature=0.1
    )
    
    raw_content = response.choices[0].message.content
    parsed_research = clean_and_parse_json(raw_content)
    return parsed_research
