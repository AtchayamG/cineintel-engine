import logging
from typing import Dict, Any, List
from app.services.parallel_service import parallel_service

logger = logging.getLogger("cineintel.mcp")

class ParallelMCPServer:
    """
    Model Context Protocol (MCP) Server adapter for Parallel Web Systems integration.
    Exposes core tools to Gemini 3.7 agents:
      1. `parallel_search_web`: Live search for film trends & tropes via Parallel Search API
      2. `parallel_extract_url`: Clean markdown/entity extraction from URLs
    """
    def __init__(self):
        self.server_name = "mcp-parallel-web"

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "parallel_search_web",
                "description": "Searches the live open web for film industry trends, cinematographic reference styles, and box office comps via Parallel Search API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"},
                        "max_results": {"type": "integer", "description": "Max results"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "parallel_extract_url",
                "description": "Extracts clean narrative tokens, entities, and summaries from a webpage URL via Parallel Extract API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "Webpage URL"}
                    },
                    "required": ["url"]
                }
            }
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Parallel MCP Call: {tool_name} with {arguments}")
        if tool_name == "parallel_search_web":
            return await parallel_service.search_open_web(
                arguments.get("query", "Cinema trends"),
                arguments.get("max_results", 4)
            )
        elif tool_name == "parallel_extract_url":
            return await parallel_service.extract_url(arguments.get("url", ""))
        return {"error": f"Tool '{tool_name}' not found"}

parallel_mcp_server = ParallelMCPServer()
