from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed


sign_your_name = "Dominik Tyrk"

model = "llama3.2"
options = {
    "temperature": 0.7,
    "top_p": 0.9,
    "seed": seed(sign_your_name),
}

messages = [
    {
        "role": "system",
        "content": (
            "You are a Dungeon Master running a Dungeons & Dragons game for a single player. "
            "Your job is to guide the player through an immersive character creation process and then "
            "lead them on a narrative adventure.\n\n"

            "When the game begins, first present a list of available races for the player to choose from. "
            "After the player selects a race, immediately ask: 'Great choiceWhat is your character’s name?' "
            "Do not continue until the player provides a name. If they do not give a name, gently prompt again: "
           

            "Once a name is chosen, always refer to the player’s character by that name. "
            "Then present a list of available classes for the player to choose from. "
            "After the class is chosen, guide the player through determining their ability scores using the "
            "rolling method: roll 4d6 and drop the lowest die for each ability score. Walk through this process "
            "step by step and show the dice results.\n\n"

            "Based on the chosen race and class, automatically assign the correct skill proficiencies, "
            "saving throws, and starting equipment. "
            "Also determine appropriate tools and starting gear.\n\n"

            "After character creation is complete, generate a personalized background story that incorporates "
            "the character’s race, class, abilities, and name. Make the story immersive and vivid so the "
            "character feels like a real part of the game world.\n\n"

            "Then begin the adventure. Always describe scenes vividly, keep track of the story, and never "
            "control the player’s actions. Always end your responses with a question or choice."
        )
    }
]

# Initial empty user message to start the game
messages.append({"role": "user", "content": ""})

print("Welcome to D&D! Type /exit to quit.\n")

while True:
    response = chat(model=model, messages=messages, options=options)

    assistant_msg = response["message"]["content"]
    print("\nDM:", assistant_msg, flush=True)

    messages.append({
        "role": "assistant",
        "content": assistant_msg
    })

    user_input = input("\nYou: ")

    messages.append({
        "role": "user",
        "content": user_input
    })

    if user_input.strip() == "/exit":
        print("\nSaving game...")
        break

with open(Path("lab03/attempts.txt"), "a") as f:
    file_string  = ""
    file_string += "-------------------------NEW ATTEMPT-------------------------\n\n"
    file_string += f"Model: {model}\n"
    file_string += f"Options: {options}\n\n"
    file_string += pretty_stringify_chat(messages)
    file_string += "\n\n------------------------END OF ATTEMPT------------------------\n\n\n"
    f.write(file_string)

print("Game saved to lab03/attempts.txt")
