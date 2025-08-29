import asyncio
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import nest_asyncio
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
nest_asyncio.apply()  # Needed to run interactive python

load_dotenv()


async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server_ai.py"],  # Arguments to the command
    )
    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            print(f"Connected to server")
            # fetch available tools
            tools = await session.list_tools()

            # Initialize OpenAI client
            llm = AzureChatOpenAI(
                deployment_name="gpt-4o",  # The name of your deployment
                model_name="gpt-4o",  # The model name
                openai_api_version="2024-12-01-preview",  # API version
                azure_endpoint="https://az-genai-3016-resource.cognitiveservices.azure.com/",
                azure_ad_token_provider=token_provider,
                temperature=0,  # Adjust temperature as needed
            )

            mcp_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in tools.tools
            ]
            for tool in mcp_tools:
                print(
                    f"Available tool: {tool['function']['name']} - {tool['function']['description']}"
                )
            agent = create_react_agent(
                llm,
                tools=mcp_tools,
                prompt="""Use the following tools to answer the user's questions. 
                        If you don't know the answer, just say you don't know. Never make up an answer.\n\n""")

            while True:
                user_input = input(
                    "Please write your question or type 'exit' to quit: "
                )
                if user_input.lower() != "exit":
                    # Call the LLM with tools
                    response = await agent.ainvoke({"messages": user_input})
                    print(response)
                    for m in response["messages"]:
                        m.pretty_print()
                else:
                    print("Exiting...")
                    break


if __name__ == "__main__":
    asyncio.run(main())
