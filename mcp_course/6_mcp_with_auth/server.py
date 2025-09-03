from fastapi import FastAPI
import contextlib
from contextlib import asynccontextmanager, AsyncExitStack
from  math_mcp import mcp
import json
from config import settings
from auth import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield

api = FastAPI(lifespan=lifespan)

# Add CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your actual origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# MCP well-known endpoint
@api.get("/.well-known/oauth-protected-resource/mcp")
async def oauth_protected_resource_metadata():
    """
    OAuth 2.0 Protected Resource Metadata endpoint for MCP client discovery.
    Required by the MCP specification for authorization server discovery.
    """

    response = json.loads(settings.METADATA_JSON_RESPONSE)
    return response


api.add_middleware(AuthMiddleware)
api.mount("/", mcp.streamable_http_app())

PORT = os.getenv("PORT", 10000)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=PORT)