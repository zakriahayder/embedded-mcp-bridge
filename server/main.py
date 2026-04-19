
from mcp.server.fastmcp import FastMCP

from server.tools.esp_bridge import register_esp_tools
from server.tools.health import register_health_tools
from server.tools.pio_tools import register_pio_tools

mcp = FastMCP("pio-esp32-mcp", log_level="ERROR")
register_pio_tools(mcp)
register_esp_tools(mcp)
register_health_tools(mcp)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
