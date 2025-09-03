from fastapi import FastAPI
from contextlib import asynccontextmanager,AsyncExitStack
from mcpservers.calc_mcp_server import mcp as math_mcp
from mcpservers.echo_mcp_server import mcp as echo_mcp
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from auth import AuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield


api = FastAPI(lifespan= lifespan)




# Add CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your actual origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)




@api.get("/.well-known/oauth-protected-resource/mcp")
async def get_oauth_math_mcp_metadata():
    """Endpoint to serve MCP metadata."""
    response =json.loads(settings.METADATA_JSON_RESPONSE)
    return response



api.add_middleware(AuthMiddleware)

api.mount("/math", math_mcp.streamable_http_app())
api.mount("/echo", echo_mcp.streamable_http_app())
api.mount("/", echo_mcp.streamable_http_app())





PORT = os.getenv("PORT", 10000)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=PORT)



