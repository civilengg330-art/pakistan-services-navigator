import json
from web_search import perform_web_search
from llm_client import get_groq_client, DEFAULT_MODEL, clean_and_parse_json
from prompts import AGENT2_SYSTEM_PROMPT

def find_sources(user_query: str, category: str, service: str) -> dict:
    """
    Performs web search and asks Agent 2 to select 2-4 authoritative sources.
    """
    search_term = f"Pakistan official {category} {service} {user_query}"
    raw_search_results = perform_web_search(search_term, max_results=6)
    
    client = get_groq_client()
    
    user_context = f"""
    User Query: {user_query}
    Category: {category}
    Subcategory/Service: {service}
    
    Raw Web Search Results:
    {json.dumps(raw_search_results, indent=2)}
    """
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": AGENT2_SYSTEM_PROMPT},
            {"role": "user", "content": user_context}
        ],
        temperature=0.2
    )
    
    raw_content = response.choices[0].message.content
    parsed_sources = clean_and_parse_json(raw_content)
    parsed_sources["raw_snippets"] = raw_search_results
    return parsed_sources
