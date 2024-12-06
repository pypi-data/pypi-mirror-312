import asyncio
import os
import logging

import mcp.server.stdio
import mcp.types as types
import unichat
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("unichat-mcp-server")

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

def validate_messages(messages):
    if len(messages) != 2:
        raise ValueError("Exactly two messages are required: one system message and one user message")

    if messages[0]["role"] != "system":
        raise ValueError("First message must have role 'system'")

    if messages[1]["role"] != "user":
        raise ValueError("Second message must have role 'user'")

def format_response(response: str) -> types.TextContent:
    """Format the response with proper structure and error handling."""
    try:
        return {"type": "text", "text": response.strip()}
    except Exception as e:
        return {"type": "text", "text": f"Error formatting response: {str(e)}"}

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="code_review",
            description="Review code for best practices, potential issues, and improvements",
            arguments=[
                types.PromptArgument(
                    name="code",
                    description="The code to review",
                    required=True
                ),
            ]
        ),
        types.Prompt(
            name="document_code",
            description="Generate documentation for code including docstrings and comments",
            arguments=[
                types.PromptArgument(
                    name="code",
                    description="The code to document",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="explain_code",
            description="Explain how a piece of code works in detail",
            arguments=[
                types.PromptArgument(
                    name="code",
                    description="The code to explain",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    prompt_templates = {
        "code_review": """You are a senior software engineer conducting a thorough code review.
            Review the following code for:
            - Best practices
            - Potential bugs
            - Performance issues
            - Security concerns
            - Code style and readability

            Code to review:
            {code}
            """,
        "document_code": """You are a technical documentation expert.
            Generate comprehensive documentation for the following code.
            Include:
            - Overview
            - Function/class documentation
            - Parameter descriptions
            - Return value descriptions
            - Usage examples

            Code to document:
            {code}
            """,
        "explain_code": """You are a programming instructor explaining code to a beginner level programmer.
            Explain how the following code works:

            {code}

            Break down:
            - Overall purpose
            - Key components
            - How it works step by step
            - Any important concepts used
            """
    }
    if name not in prompt_templates:
        logger.error(f"Unknown prompt: {name}")
        raise ValueError(f"Unknown prompt: {name}")

    if not arguments or "code" not in arguments:
        logger.error("Missing required argument: code")
        raise ValueError("Missing required argument: code")

    code = arguments["code"]

    # Format the template with provided arguments
    system_content = prompt_templates[name].format(code=code)

    try:
        response = chat_api.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": "Please provide your analysis."}
            ],
            stream=False
        )
        return types.GetPromptResult(
            description=f"Requested code manipulation",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=format_response(response),
                )
            ],
        )
    except Exception as e:
        logger.error(f"Error in prompt {name}: {e}")
        raise Exception(f"An error occurred: {e}")


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

    try:
        validate_messages(arguments.get("messages", []))

        response = chat_api.chat.completions.create(
            model=MODEL,
            messages=arguments["messages"],
            stream=False
        )

        return [format_response(response)]
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        raise Exception(f"An error occurred: {e}")

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