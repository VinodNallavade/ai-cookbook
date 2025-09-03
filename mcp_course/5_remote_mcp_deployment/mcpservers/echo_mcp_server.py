from mcp.server.fastmcp import FastMCP
import os

PORT = os.getenv("PORT", 10000)

mcp = FastMCP(name="Echo",host="0.0.0.0",port=PORT)

@mcp.tool()
def echo_message(message: str) -> str:
    """Echo the input message."""
    return message


if __name__ == "__main__":  
    mcp.run(transport="streamable-http")    