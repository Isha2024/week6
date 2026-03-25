# Week 6: Model Context Protocol (MCP)

Blueprint AI Fellowship | Spring 2026

## Files

- `main.py` - The MCP client. Hit Run to start. (Parts 2 and 3)
- `server.py` - The MCP server. Defines the tools. (Parts 1 and 3)
- `requirements.txt` - Python packages to install

## Quick Start

1. Open Shell and run: `pip install mcp httpx requests`
2. Make sure `GROQ_API_KEY` is in your Secrets tab
3. Hit the green Run button

## How It Works

When you hit Run, `main.py` does three things:

1. Spawns `server.py` as a subprocess
2. Connects to it using the MCP protocol
3. Discovers and calls the tools it exposes

You will edit `server.py` to add your own project tools, then
test them by running `main.py` again.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError: mcp | Run: `pip install mcp httpx requests` |
| Server won't connect | Check for syntax errors in server.py: `python server.py` |
| Tool not showing up | Add @mcp.tool() decorator and restart |
