import requests
from mcp.server.fastmcp import FastMCP

_connection: dict | None = None


def _connect(ip: str, port: int = 80) -> dict:
    global _connection
    try:
        resp = requests.get(f"http://{ip}:{port}/tools", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        tools = [t["name"] for t in data.get("tools", [])]
        # Update the global connection variable
        _connection = {"ip": ip, "port": port, "tools": tools}
        return {"success": True, "available_tools": tools}
    except requests.Timeout:
        return {"success": False, "error": f"Cannot reach {ip}:{port}"}
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

def _call(tool_name: str, args: dict) -> dict:
    global _connection
    if _connection is None:
        return {"success": False, "error": "Not connected. Call esp_connect first."}
    ip, port = _connection["ip"], _connection["port"]
    try:
        resp = requests.post(
            f"http://{ip}:{port}/call",
            json={"tool": tool_name, "args": args},
            timeout=10,
        )
        resp.raise_for_status()
        return {"success": True, "result": resp.json()}
    except requests.Timeout:
        return {"success": False, "error": f"Timeout calling {tool_name}"}
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

def _disconnect() -> dict:
    global _connection
    _connection = None
    return {"success": True}


def register_esp_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    def esp_connect(ip: str, port: int = 80) -> dict:
        """Connect to ESP32 server at given IP."""
        return _connect(ip, port)

    @mcp.tool()
    def esp_call(tool_name: str, args: dict = {}) -> dict:
        """Call a tool on the connected ESP32."""
        return _call(tool_name, args)

    @mcp.tool()
    def esp_disconnect() -> dict:
        """Close the connection."""
        return _disconnect()
