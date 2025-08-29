# AI Cookbook

This repository contains example code for building simple AI agent servers and clients using Python.

## Structure

- `mcp/2-simple-server-setup/`
  - `server.py`: Implements a calculator server using FastMCP with tools for addition and evaluating mathematical expressions.
  - `client-stdio.py`: Interactive client that connects to the server via stdio, allowing users to evaluate expressions.
  - `client-sse.py`: (Reserved for SSE client implementation.)
- `mcp/3-openai-integration/`: (Reserved for OpenAI integration examples.)
- `.env`: Environment variables for configuration.
- `requirements.txt`: Python dependencies.

## Getting Started

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```sh
   cd mcp/2-simple-server-setup
   python server.py
   ```

3. **Run the client:**
   ```sh
   python client-stdio.py
   ```

4. **Usage:**
   - Enter mathematical expressions (e.g., `2+2`, `3*5`) in the client prompt.
   - Type `exit` to quit.

## Features

- Simple calculator server with addition and expression evaluation tools.
- Interactive client-server communication using stdio transport.
- Easily extensible for more tools and transports.
