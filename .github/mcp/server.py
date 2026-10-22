from mcp.server.fastmcp import FastMCP


mcp = FastMCP("cityops-tools")


MISSIONS = {
    "DEV-001": {
        "title": "Add incident priority endpoint",
        "status": "ready",
        "owner": "software-development"
    },
    "SEC-001": {
        "title": "Review incident API security",
        "status": "ready",
        "owner": "security"
    }
}


@mcp.tool()
def get_mission_status(mission_id: str) -> dict:
    """Get the current status of a CityOps development mission."""

    mission = MISSIONS.get(mission_id)

    if mission is None:
        return {
            "mission_id": mission_id,
            "status": "not-found"
        }

    return {
        "mission_id": mission_id,
        **mission
    }


@mcp.tool()
def list_missions() -> list:
    """List available CityOps development missions."""

    return list(MISSIONS.keys())


if __name__ == "__main__":
    mcp.run()