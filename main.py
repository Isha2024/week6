# ============================================================
# WEEK 6: MCP CLIENT
# ============================================================
# This file connects to your MCP server (server.py), discovers
# its tools, and calls them.
#
# Hit the green Run button to start. This will:
#   1. Spawn server.py as a subprocess
#   2. Connect to it using the MCP protocol
#   3. Discover what tools are available
#   4. Call those tools and print the results
#
# This is the same pattern that happens inside Claude Desktop
# or Cursor when they connect to an MCP server. You are
# building the client side to understand how it works.
# ============================================================

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # ============================================================
    # PART 2: CONNECT A CLIENT TO YOUR SERVER
    # ============================================================
    # The client does not know what tools the server has.
    # It discovers them at connection time. This is what makes
    # MCP portable: the server advertises its capabilities and
    # any compatible client can use them.
    # ============================================================

    print("=" * 55)
    print("  WEEK 6: Model Context Protocol (MCP)")
    print("=" * 55)
    print()

    # Tell the client how to start the server
    # "command" and "args" are like running: python server.py
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
        env={
            **os.environ,
            "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
        }
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Step 1: Initialize the connection
            await session.initialize()
            print("[Connected to MCP server]")
            print()

            # Step 2: Discover available tools
            # The client asks: "What can you do?"
            # The server responds with a list of tools, their
            # descriptions, and their parameter schemas.
            tools_response = await session.list_tools()
            tools = tools_response.tools

            print("-" * 55)
            print(f"  DISCOVERED {len(tools)} TOOLS")
            print("-" * 55)
            for tool in tools:
                print(f"  {tool.name}")
                print(f"    {tool.description}")
                if tool.inputSchema and "properties" in tool.inputSchema:
                    params = list(tool.inputSchema["properties"].keys())
                    print(f"    Parameters: {', '.join(params)}")
                print()

            # Step 3: Call a tool
            # The client sends: "Run this tool with these arguments"
            # The server executes the function and returns the result.
            print("-" * 55)
            print("  CALLING: get_weather")
            print("-" * 55)

            result = await session.call_tool(
                "get_weather",
                {"city": "New Brunswick"}
            )
            print(f"  Result: {result.content[0].text}")
            print()

            # Call another tool
            print("-" * 55)
            print("  CALLING: calculate")
            print("-" * 55)

            result = await session.call_tool(
                "calculate",
                {"expression": "15 * 4 + 10"}
            )
            print(f"  Result: {result.content[0].text}")
            print()

            # ============================================================
            # PART 3: TEST YOUR PROJECT'S TOOLS
            # ============================================================
            # After adding tools to server.py, test them here.
            # Uncomment and modify the example below.
            #
            # print("-" * 55)
            # print("  CALLING: your_tool_name")
            # print("-" * 55)
            #
            # result = await session.call_tool(
            #     "your_tool_name",
            #     {"param_name": "param_value"}
            # )
            # print(f"  Result: {result.content[0].text}")
            # print()
            # ============================================================

            print("=" * 55)
            print("  DONE")
            print("=" * 55)
            print()
            print("What just happened:")
            print("  1. main.py spawned server.py as a subprocess")
            print("  2. Connected using the MCP protocol (STDIO)")
            print("  3. Discovered tools the server exposes")
            print("  4. Called tools and got results back")
            print()
            print("This is the same pattern Claude Desktop uses")
            print("when it connects to an MCP server.")
            print()
            print("Next: open server.py and add your project's tools.")
            print("Then uncomment Part 3 above and test them.")


if __name__ == "__main__":
    asyncio.run(main())
