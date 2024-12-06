import asyncio
from typing import Any
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("mcp-simple-timeserver")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_time",
            description="Returns the current local time and timezone information.",
            inputSchema={
                "type": "object",
                # Even though we don't have any required inputs, we should define the schema
                "properties": {},
                "additionalProperties": False  # This ensures no unexpected inputs
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:  # Note: should return a list of TextContent
    if name == "get_time":
        local_time = datetime.now()
        timezone = str(datetime.now().astimezone().tzinfo)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
        response = f"Current Time: {formatted_time}\nTimezone: {timezone}"
        return [TextContent(type="text", text=response)]  # Wrap in a list and properly construct TextContent
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream, app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())