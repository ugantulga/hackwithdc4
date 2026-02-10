"""
Linkup MCP Tool Wrapper for LangChain
Provides web search capabilities through Linkup's API
"""
import os
import requests
from typing import Optional, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import Field


class LinkupSearchTool(BaseTool):
    """Tool for searching the web using Linkup API"""
    
    name: str = "linkup_search"
    description: str = """
    Search the web in real-time to retrieve current information, facts, and news.
    Use this when you need:
    - Current information beyond training data cutoff
    - Verification of facts or statistics
    - Recent news or events
    - Company/organization information
    - Research on unfamiliar topics
    
    Input should be a natural language search query.
    Returns structured search results with sources.
    """
    
    api_key: str = Field(default_factory=lambda: os.getenv("LINKUP_API_KEY", ""))
    base_url: str = "https://api.linkup.so/v1/search"
    
    def _run(self, query: str, depth: str = "standard") -> str:
        """
        Execute web search using Linkup API
        
        Args:
            query: Natural language search query
            depth: "standard" or "deep" (deep is slower but more comprehensive)
        
        Returns:
            Formatted search results with sources
        """
        if not self.api_key:
            return "Error: LINKUP_API_KEY not set. Please configure your API key."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": query,
                "depth": depth,
                "outputType": "sourcedAnswer"  # Get answer with sources
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response
            if "answer" in data:
                answer = data["answer"]
                sources = data.get("sources", [])
                
                result = f"Answer: {answer}\n\n"
                
                if sources:
                    result += "Sources:\n"
                    for i, source in enumerate(sources[:5], 1):  # Limit to top 5
                        title = source.get("title", "Unknown")
                        url = source.get("url", "")
                        result += f"{i}. {title}\n   {url}\n"
                
                return result
            else:
                return f"Search completed but no direct answer found. Raw results: {data}"
                
        except requests.exceptions.RequestException as e:
            return f"Error performing web search: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version - for now just call sync version"""
        return self._run(query)


class LinkupDeepSearchTool(BaseTool):
    """Tool for deep web search using Linkup API (more comprehensive but slower)"""
    
    name: str = "linkup_deep_search"
    description: str = """
    Perform DEEP web search for complex research requiring analysis across multiple sources.
    Use this for:
    - Comprehensive research topics
    - Comparative analysis
    - In-depth investigations
    - Topics requiring multiple perspectives
    
    This is slower than regular search but provides more thorough results.
    Input should be a detailed research question.
    """
    
    api_key: str = Field(default_factory=lambda: os.getenv("LINKUP_API_KEY", ""))
    base_url: str = "https://api.linkup.so/v1/search"
    
    def _run(self, query: str) -> str:
        """Execute deep web search"""
        if not self.api_key:
            return "Error: LINKUP_API_KEY not set."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": query,
                "depth": "deep",  # Deep search for comprehensive results
                "outputType": "sourcedAnswer"
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60  # Longer timeout for deep search
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "answer" in data:
                answer = data["answer"]
                sources = data.get("sources", [])
                
                result = f"Deep Search Results:\n\n{answer}\n\n"
                
                if sources:
                    result += "Sources (showing top 10):\n"
                    for i, source in enumerate(sources[:10], 1):
                        title = source.get("title", "Unknown")
                        url = source.get("url", "")
                        snippet = source.get("snippet", "")
                        result += f"\n{i}. {title}\n"
                        result += f"   URL: {url}\n"
                        if snippet:
                            result += f"   Preview: {snippet[:150]}...\n"
                
                return result
            else:
                return f"Deep search completed. Results: {data}"
                
        except Exception as e:
            return f"Error performing deep search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version"""
        return self._run(query)


def create_linkup_tools() -> List[BaseTool]:
    """
    Create and return all Linkup tools
    
    Returns:
        List of Linkup tools ready to use with LangChain agents
    """
    return [
        LinkupSearchTool(),
        LinkupDeepSearchTool()
    ]


# For testing
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    tools = create_linkup_tools()
    
    # Test standard search
    search_tool = tools[0]
    result = search_tool.run("What are the latest developments in AI?")
    print("Standard Search Result:")
    print(result)
    print("\n" + "="*80 + "\n")
    
    # Test deep search
    deep_search_tool = tools[1]
    result = deep_search_tool.run("Compare the top 3 LLM models released in 2024")
    print("Deep Search Result:")
    print(result)
