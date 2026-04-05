The initialize method is called first when a client connects to a server. This establishes the connection and allows the client and server to exchange capabilities.
tools/list returns a list of available tools provided by the server. Each tool includes its name, description, and input schema so the client knows how to use it.
A tools/call request includes the tool name to invoke, the arguments for the tool, and a request ID. It is formatted as a JSON-RPC request with "method": "tools/call" and a "params" object containing the tool name and arguments.
In Lab 05, manual tool calling required explicitly deciding when to call a tool, formatting the request, and handling responses step by step. With MCP + LangGraph, much of this work is automated. LangGraph manages the flow of decisions, tool selection, and chaining actions together. MCP provides a standardized way for tools to be defined and accessed, making systems more modular, reusable, and easier to scale.
MCP could allow the Dungeon Master system to dynamically access tools like a monster lookup tool that returns stats, abilities, and weaknesses, a dice rolling tool that handles random rolls with rules, or a map generation tool that creates dungeon layouts. For example, when a player encounters an enemy, the system could call the monster tool to retrieve stats automatically instead of relying on preloaded data.

Tools: roll_dice, get_character_stat, calculate_damage
[OK] Connected to MCP server!

Found 3 tools:
  - roll_dice: Rolls a dice and then adds a modifier to the result
  - get_character_stat: Get a character's stat value
  - calculate_damage: Calculate damage dealt based on attack roll vs armor class

------------------------------------------------------------
Chat with the DnD assistant (type 'quit' to exit)
Try: 'Roll a d20 for an attack' or 'What is the fighter's strength?'
------------------------------------------------------------

You: roll a d20 foran attack

Assistant: The roll result is a 20. Is there anything else you'd like assistance with, such as applying this to an attack roll?

You: what is the fighter's strength

Assistant: I've looked up the fighter character stat and their strength is indeed 16. Let me know if you need help with anything else!
