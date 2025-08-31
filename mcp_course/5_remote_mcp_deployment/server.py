from fastapi import FastAPI
from contextlib import asynccontextmanager,AsyncExitStack
from mcpsevers.calc_mcp_server import mcp as math_mcp
from mcpsevers.echo_mcp_server import mcp as echo_mcp
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield


api = FastAPI(lifespan= lifespan)
api.mount("/math", math_mcp.streamable_http_app())
api.mount("/echo", echo_mcp.streamable_http_app())


PORT = os.getenv("PORT", 10000)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=PORT)



