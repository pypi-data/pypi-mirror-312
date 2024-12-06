from typing import Annotated
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field
from tavily import TavilyClient, InvalidAPIKeyError, UsageLimitExceededError

from typing import Literal

class SearchBase(BaseModel):
    """Base parameters for Tavily search."""
    query: Annotated[str, Field(description="Search query")]
    max_results: Annotated[
        int,
        Field(
            default=5,
            description="Maximum number of results to return",
            gt=0,
            lt=20,
        ),
    ]

class GeneralSearch(SearchBase):
    """Parameters for general web search."""
    search_depth: Annotated[
        Literal["basic", "advanced"],
        Field(
            default="basic",
            description="Depth of search - 'basic' or 'advanced'",
        ),
    ]

class AnswerSearch(SearchBase):
    """Parameters for search with answer."""
    search_depth: Annotated[
        Literal["basic", "advanced"],
        Field(
            default="advanced",
            description="Depth of search - 'basic' or 'advanced'",
        ),
    ]

class NewsSearch(SearchBase):
    """Parameters for news search."""
    days: Annotated[
        int | None,
        Field(
            default=None,
            description="Number of days back to search (default is 3)",
            gt=0,
            lt=365,
        ),
    ]

async def serve(api_key: str) -> None:
    """Run the Tavily MCP server.

    Args:
        api_key: Tavily API key
    """
    server = Server("mcp-tavily")
    client = TavilyClient(api_key=api_key)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="tavily_web_search",
                description="""Performs a comprehensive web search using Tavily's AI-powered search engine. 
                Excels at extracting and summarizing relevant content from web pages, making it ideal for research, 
                fact-finding, and gathering detailed information. Can run in either 'basic' mode for faster, simpler searches 
                or 'advanced' mode for more thorough analysis. Returns multiple search results with AI-extracted relevant content.""",
                inputSchema=GeneralSearch.model_json_schema(),
            ),
            Tool(
                name="tavily_answer_search",
                description="""Performs a web search using Tavily's AI search engine and generates a direct answer to the query, 
                along with supporting search results. Best used for questions that need concrete answers backed by current web sources. 
                Uses advanced search depth by default for comprehensive analysis. Particularly effective for factual queries, 
                technical questions, and queries requiring synthesis of multiple sources.""",
                inputSchema=AnswerSearch.model_json_schema(),
            ),
            Tool(
                name="tavily_news_search",
                description="""Searches recent news articles using Tavily's specialized news search functionality. 
                Ideal for current events, recent developments, and trending topics. Can filter results by recency 
                (number of days back to search), making it perfect for tracking recent news on specific topics or 
                monitoring ongoing developments. Returns news articles with publication dates and relevant excerpts.""",
                inputSchema=NewsSearch.model_json_schema(),
            ),
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="tavily_web_search",
                description="Search the web using Tavily's AI-powered search engine",
                arguments=[
                    PromptArgument(
                        name="query",
                        description="Search query",
                        required=True,
                    )
                ],
            ),
            Prompt(
                name="tavily_answer_search",
                description="Search the web and get an AI-generated answer with supporting evidence",
                arguments=[
                    PromptArgument(
                        name="query",
                        description="Search query",
                        required=True,
                    )
                ],
            ),
            Prompt(
                name="tavily_news_search",
                description="Search recent news articles with Tavily's news search",
                arguments=[
                    PromptArgument(
                        name="query",
                        description="Search query",
                        required=True,
                    ),
                    PromptArgument(
                        name="days",
                        description="Number of days back to search",
                        required=False,
                    ),
                ],
            ),
        ]

    def format_results(response: dict) -> str:
        """Format Tavily search results into a readable string."""
        output = []
        
        if response.get("answer"):
            output.append(f"Answer: {response['answer']}\n")
        
        output.append("Search Results:")
        for result in response["results"]:
            output.append(f"\nTitle: {result['title']}")
            output.append(f"URL: {result['url']}")
            output.append(f"Content: {result['content']}")
            if result.get("published_date"):
                output.append(f"Published: {result['published_date']}")
            
        return "\n".join(output)

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "tavily_web_search":
                args = GeneralSearch(**arguments)
                response = client.search(
                    query=args.query,
                    max_results=args.max_results,
                    search_depth=args.search_depth,
                )
            elif name == "tavily_answer_search":
                args = AnswerSearch(**arguments)
                response = client.search(
                    query=args.query,
                    max_results=args.max_results,
                    search_depth=args.search_depth,
                    include_answer=True,
                )
            elif name == "tavily_news_search":
                args = NewsSearch(**arguments)
                response = client.search(
                    query=args.query,
                    max_results=args.max_results,
                    topic="news",
                    days=args.days if args.days is not None else 3,
                )
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except (InvalidAPIKeyError, UsageLimitExceededError) as e:
            raise McpError(INTERNAL_ERROR, str(e))
        except ValueError as e:
            raise McpError(INVALID_PARAMS, str(e))

        return [TextContent(
            type="text",
            text=format_results(response),
        )]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if not arguments or "query" not in arguments:
            raise McpError(INVALID_PARAMS, "Query is required")

        try:
            if name == "tavily_web_search":
                response = client.search(query=arguments["query"])
            elif name == "tavily_answer_search":
                response = client.search(
                    query=arguments["query"],
                    include_answer=True,
                    search_depth="advanced",
                )
            elif name == "tavily_news_search":
                days = arguments.get("days")
                response = client.search(
                    query=arguments["query"],
                    topic="news",
                    days=int(days) if days else 3,
                )
            else:
                raise McpError(INVALID_PARAMS, f"Unknown prompt: {name}")

        except (InvalidAPIKeyError, UsageLimitExceededError) as e:
            return GetPromptResult(
                description=f"Failed to search: {str(e)}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=str(e)),
                    )
                ],
            )

        return GetPromptResult(
            description=f"Search results for: {arguments['query']}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=format_results(response)),
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

if __name__ == "__main__":
    import asyncio
    import os
    
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is required")
        
    asyncio.run(serve(api_key))