"""
DnD MCP Server - Lab 11
===================================
Complete implementation of the MCP server with three DnD-related tools.
"""

import random
from fastmcp import FastMCP


# Sample character data - use this for get_character_stat
CHARACTERS = {
    "fighter": {
        "strength": 16,
        "dexterity": 14,
        "constitution": 15,
        "intelligence": 10,
        "wisdom": 12,
        "charisma": 8
    },
    "wizard": {
        "strength": 8,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 15,
        "charisma": 10
    },
    "rogue": {
        "strength": 10,
        "dexterity": 18,
        "constitution": 12,
        "intelligence": 14,
        "wisdom": 10,
        "charisma": 14
    }
}

# =====================================================================
# TODO: Implement the three tool functions below.
# Each function should return a string with the result message.
# =====================================================================


def roll_dice(n_dice: int, sides: int, modifier: int = 0) -> str:
    try:
        n_dice = int(n_dice)
        sides = int(sides)
        modifier = int(modifier) if modifier is not None else 0
    except (ValueError, TypeError):
        return "Error: Invalid input types. Please provide integers."

    rolls = [random.randint(1, sides) for _ in range(n_dice)]
    total = sum(rolls) + modifier
    return f"Rolled {n_dice}d{sides}+{modifier}: {rolls} + {modifier} = {total}"

    


@mcp.tool()
def get_character_stat(character: str, stat: str) -> str:
    character = character.lower()
    stat = stat.lower()

    if character not in CHARACTERS:
        return f"Error: Unknown character '{character}'"

    if stat not in CHARACTERS[character]:
        return f"Error: Unknown stat '{stat}' for {character}"

    value = CHARACTERS[character][stat]
    return f"{character.capitalize()}'s {stat} is {value}"
    


@mcp.tool()
def calculate_damage(base_damage: int, armor_class: int, attack_roll: int) -> str:
    try:
        base_damage = int(base_damage)
        armor_class = int(armor_class)
        attack_roll = int(attack_roll)
    except (ValueError, TypeError):
        return "Error: Invalid input types."

    if attack_roll >= armor_class:
        return f"Attack hits! Dealt {base_damage} damage."
    else:
        return "Attack misses! Dealt 0 damage."
    


# =====================================================================
# MCP Server wiring — tool schemas and call_tool dispatcher
# You should NOT need to modify anything below this line.
# =====================================================================

# Create the MCP server instance
server = Server("dnd-tools-server")

# Map tool names to their implementation functions
TOOL_FUNCTIONS = {
    "roll_dice": roll_dice,
    "get_character_stat": get_character_stat,
    "calculate_damage": calculate_damage,
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available DnD tools.

    TODO: Define three tools with their input schemas:

    1. roll_dice:
       - n_dice (int): Number of dice to roll
       - sides (int): Number of sides on each die
       - modifier (int, optional): Modifier to add to the roll (default 0)

    2. get_character_stat:
       - character (str): Character name (fighter, wizard, or rogue)
       - stat (str): Stat name (strength, dexterity, constitution, intelligence, wisdom, charisma)

    3. calculate_damage:
       - base_damage (int): Base damage amount
       - armor_class (int): Target's armor class
       - attack_roll (int): The attack roll result

    See demo/simple_mcp_server.py for the Tool schema format.
    """
    return [
        # TODO: Define your tools here
        # Example:
        # Tool(
        #     name="roll_dice",
        #     description="Roll dice for DnD",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "n_dice": {"type": "integer", "description": "Number of dice"},
        #             ...
        #         },
        #         "required": ["n_dice", "sides"]
        #     }
        # ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Dispatch tool calls to the corresponding function."""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    result = func(**arguments)
    return [TextContent(type="text", text=result)]


async def main():
    """Run the DnD MCP server."""
    import sys
    # Use stderr for logging since stdout is used for JSON-RPC protocol
    print("Starting DnD MCP server...", file=sys.stderr, flush=True)
    print("Tools: roll_dice, get_character_stat, calculate_damage", file=sys.stderr, flush=True)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
