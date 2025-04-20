import yaml
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from contextlib import AsyncExitStack

async def load_mcp_toolset(path: str):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    urls = [entry.get("url") for entry in config.get("tools", []) if entry.get("url")]

    if not urls:
        print("[INFO] No URL found in config_sse_tools.yaml. No remote MCP tools will be loaded.")
        return [], AsyncExitStack()

    all_tools = []
    exit_stack = AsyncExitStack()

    for url in urls:
        conn = SseServerParams(url=url)
        try:
            tools, _ = await MCPToolset.from_server(connection_params=conn)
            await exit_stack.enter_async_context(_)
            all_tools.extend(tools)
            print(f"[INFO] MCP tools loaded with {url}")
        except Exception as e:
            print(f"[ERROR] Failed to connect to MCP tool on {url} — {e}")

    return all_tools, exit_stack

