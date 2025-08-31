from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Calculator",
              host="0.0.0.0",
                port=8050,
              )

@mcp.tool() 
def add_numbers(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool() 
def subtract_numbers(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

@mcp.tool()
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers."""   
    if b == 0:
        raise ValueError("Cannot divide by zero.")      
    return a / b


if __name__ == "__main__":
    transport ="stdio"  
    if transport == "sse":
        mcp.run(transport="sse")
        print("Connected to http://localhost:8050 using sse transport") 
    elif transport == "stdio":
        mcp.run(transport="stdio")
        print("Connected using stdio transport")    
    else:
        print("invalid transport, please choose either 'sse' or 'stdio'")    