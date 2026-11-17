import asyncio
import json
import os
from pathlib import Path

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_configured_mcp_server(tmp_path):
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / ".vscode" / "mcp.json").read_text())
    server = config["servers"]["software-dev-tools"]
    args = [
        arg.replace("${workspaceFolder}", str(root))
        for arg in server["args"]
    ]
    env = {
        key: value.replace("${workspaceFolder}", str(root))
        for key, value in server.get("env", {}).items()
    }

    async def check_server():
        with anyio.fail_after(20):
            params = StdioServerParameters(
                command=server["command"],
                args=args,
                env={**os.environ, **env},
                cwd=str(tmp_path),
            )
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    assert {tool.name for tool in tools.tools} == {
                        "list_tasks", "get_task_details", "validate_plan"
                    }
                    tasks = await session.call_tool("list_tasks", {})
                    assert not tasks.isError
                    details = await session.call_tool(
                        "get_task_details", {"task_id": 1}
                    )
                    assert not details.isError
                    task = json.loads(details.content[0].text)
                    assert task == {
                        "id": 1,
                        "title": "Create login module",
                        "priority": "high",
                        "status": "open",
                    }

    asyncio.run(check_server())
