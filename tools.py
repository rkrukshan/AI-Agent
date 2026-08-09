from datetime import datetime
import wikipedia
from langchain.tools import Tool

# 1. Reliable Wikipedia Tool
# We must set a custom User-Agent, otherwise Wikipedia blocks the API request and returns a JSONDecodeError
wikipedia.set_user_agent("AIAgentResearchBot/1.0 (contact@example.com)")

def wiki_search(query: str) -> str:
    """Queries Wikipedia for topic summaries."""
    try:
        # Fetch the top summary directly
        return wikipedia.summary(query, sentences=5)
    except wikipedia.exceptions.DisambiguationError as e:
        # If the search term is too broad (e.g., "Python"), pick the first specific option
        return wikipedia.summary(e.options[0], sentences=5)
    except wikipedia.exceptions.PageError:
        return "Wikipedia page not found."
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

wiki_tool = Tool(
    name="wikipedia",
    func=wiki_search,
    description="Query Wikipedia for structured topic summaries and historical context."
)

# 2. Reliable DuckDuckGo Search Tool
def ddg_search(query: str) -> str:
    """Performs web search using DuckDuckGo directly."""
    try:
        from duckduckgo_search import DDGS
        # Using the standard text search API
        results = DDGS().text(query, max_results=3)
        
        if not results:
            return "No search results found."
            
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nURL: {r.get('href')}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Search error: {str(e)}"

search_tool = Tool(
    name="search",
    func=ddg_search,
    description="Search the web for current facts, news, and general knowledge."
)

# 3. Custom File Saver Tool
def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_data = f"Research Output - {timestamp}\n\n{data}"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_data)
        
    return f"Saved successfully to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Save research data to a text file."
)