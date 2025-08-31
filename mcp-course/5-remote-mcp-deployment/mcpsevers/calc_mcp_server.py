from mcp.server.fastmcp import FastMCP
import os

PORT = os.getenv("PORT", 10000)


mcp = FastMCP(name="Calculator".host="0.0.0.0",port=PORT)

@mcp.tool()
def add_numbers(a: float, b: float) -> float:   
    """Add two numbers."""
    return a + b


if __name__ == "__main__":  
    mcp.run(transport="streamable-http")