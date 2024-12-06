import asyncio
import os

import mcp.server.stdio
import mcp.types as types
import unichat
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Initialize the server
server = Server("unichat-mcp-server")

# API configuration
MODEL = os.getenv("UNICHAT_MODEL")
if not MODEL:
    raise ValueError("UNICHAT_MODEL environment variable required")
UNICHAT_API_KEY = os.getenv("UNICHAT_API_KEY")
if not UNICHAT_API_KEY:
    raise ValueError("UNICHAT_API_KEY environment variable required")

chat_api = unichat.UnifiedChatApi(api_key=UNICHAT_API_KEY)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="unichat",
            description="""Chat with the assistant. Messages must follow a specific structure:
            - First message should be a system message defining the task or context
            - Second message should be a user message containing the specific query or request

            Example structure:
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant focused on answering questions about Python programming"},
                    {"role": "user", "content": "How do I use list comprehensions?"}
                ]
            }""",
            inputSchema={
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {
                                    "type": "string",
                                    "description": "The role of the message sender. Must be either 'system' or 'user'",
                                    "enum": ["system", "user"]
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The content of the message. For system messages, this should define the context or task. For user messages, this should contain the specific query."
                                },
                            },
                            "required": ["role", "content"],
                        },
                        "minItems": 2,
                        "maxItems": 2,
                        "description": "Array of exactly two messages: first a system message defining the task, then a user message with the specific query"
                    },
                },
                "required": ["messages"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name != "unichat":
        raise ValueError(f"Unknown tool: {name}")

    if len(arguments.get("messages", [])) != 2:
        raise ValueError("Exactly two messages are required: one system message and one user message")

    if arguments["messages"][0]["role"] != "system":
        raise ValueError("First message must have role 'system'")

    if arguments["messages"][1]["role"] != "user":
        raise ValueError("Second message must have role 'user'")

    try:
        response = chat_api.chat.completions.create(
            model=MODEL,
            messages=arguments["messages"],
            stream=False
        )
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

    return [{"type": "text", "text": response}]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="unichat-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())