import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging

logging.basicConfig(level=logging.INFO)

nest_asyncio.apply()  # Needed to run interactive python


async def run():
    try:
        # Define server parameters
        server_params = StdioServerParameters(
            command="python",  # The command to run your server
            args=["server.py"],  # Arguments to the command
        )
        # Connect to the server
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                await session.initialize()
                #print(f"Connected to server: {session.server_info.name}")
                while True:
                    expression = input("Enter a mathematical expression like  2+2 or 2*3 or type 'exit' to quit: ")
                    if expression.lower() != 'exit':
                        # Call the evaluate_expression tool
                        eval_result = await session.call_tool("evaluate_expression", arguments={"expression": expression})
                        print(f"Result: {eval_result.content[0].text}")
                    else:
                        print("Exiting...")
                        break    
    except Exception as e:
        logging.error(f"An error occurred: {e}")            


if __name__ == "__main__":
    asyncio.run(run())