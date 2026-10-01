from duckduckgo_search import DDGS

def perform_web_search(query: str, max_results: int = 5) -> list:
    """
    Performs runtime DuckDuckGo web search.
    Returns a list of dictionaries with title, href, and body.
    """
    results = []
    try:
        with DDGS() as ddgs:
            search_gen = ddgs.text(query, region="pk-en", max_results=max_results)
            if search_gen:
                for r in search_gen:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
    except Exception as e:
        print(f"Web search error: {e}")
        # Fallback query with broader region if pk-en fails
        try:
            with DDGS() as ddgs:
                search_gen = ddgs.text(f"Pakistan {query}", max_results=max_results)
                if search_gen:
                    for r in search_gen:
                        results.append({
                            "title": r.get("title", ""),
                            "url": r.get("href", ""),
                            "snippet": r.get("body", "")
                        })
        except Exception as inner_e:
            print(f"Fallback web search error: {inner_e}")
            
    return results
