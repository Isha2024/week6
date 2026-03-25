# ============================================================
# WEEK 6: YOUR MCP SERVER
# ============================================================
# This file defines your MCP server. It exposes tools that
# any MCP-compatible client can discover and use.
#
# Think of this file as a standalone program that wraps your
# tools in the MCP protocol. Any MCP-compatible host (Claude
# Desktop, Cursor, Windsurf, or our client in main.py) can
# connect to this server and use these tools.
#
# Part 1: A basic server with two tools
# Part 3: Add your own project tools here
# ============================================================

from mcp.server.fastmcp import FastMCP
import requests
import os

# Create the server with a name
# This name shows up when clients connect
mcp = FastMCP("blueprint-tools")


# ============================================================
# PART 1: YOUR FIRST MCP TOOLS
# ============================================================
# These tools do the same things as the functions from Weeks 4
# and 5. The difference: they live in their own server program
# instead of being hardcoded into your application.
#
# The @mcp.tool() decorator does three things:
#   1. Registers the function as an MCP tool
#   2. Uses the docstring as the tool description
#   3. Uses the type hints as the parameter schema
#
# Compare this to CrewAI's @tool decorator from Week 5.
# Same idea, different protocol.
# ============================================================

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city. Returns temperature, conditions, and humidity."""
    url = f"https://wttr.in/{city}?format=%C+%t+%h"
    try:
        response = requests.get(url, timeout=5)
        return f"Weather in {city}: {response.text.strip()}"
    except Exception as e:
        return f"Could not get weather for {city}: {e}"


@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a math expression. Examples: '2 + 2', '100 * 0.15', '(50 + 30) / 4'."""
    try:
        # Only allow safe math characters
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "Error: only numbers and basic math operators are allowed"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


# ============================================================
# PART 3: ADD YOUR PROJECT'S TOOLS BELOW
# ============================================================
# Take one or two tools from your final project (the functions
# you built in Weeks 4 and 5) and wrap them as MCP tools.
#
# Steps:
#   1. Copy your function here
#   2. Add @mcp.tool() above it
#   3. Add a clear docstring (this is what the client sees)
#   4. Add type hints to the parameters
#   5. Restart the server and test from main.py
#
# Example for a study assistant project:
#
# @mcp.tool()
# def search_courses(query: str) -> str:
#     """Search the course catalog for classes matching a query.
#     Returns course names, descriptions, and schedule info."""
#     # Your search logic here (could query Pinecone, a database, etc.)
#     return results
#
# Example for a recipe project:
#
# @mcp.tool()
# def find_recipes(ingredients: str) -> str:
#     """Find recipes that use the given ingredients.
#     Pass ingredients as a comma-separated string."""
#     # Your recipe search logic here
#     return results

# --- YOUR PROJECT TOOLS GO HERE ---




# ============================================================
# Start the server
# ============================================================
# This runs the server using STDIO transport, which means it
# communicates through standard input/output. The client in
# main.py spawns this as a subprocess and talks to it through
# those streams.
#
# You do not need to modify anything below this line.
# ============================================================

if __name__ == "__main__":
    mcp.run()
