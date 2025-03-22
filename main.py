from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCPXcode")

@mcp.tool()
async def get_mcpxcode() -> str:
    """Print Summary
    """
    return "Hello MCPXcode :) MCPXcode is MCP server for Xcode."


if __name__ == "__main__":
    mcp.run(transport='stdio')