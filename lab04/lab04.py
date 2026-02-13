from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import TemplateChat


BASE = Path(__file__).parent

DM_TEMPLATE = BASE / "lab04_dm.json"
NPC_TEMPLATE = BASE / "lab04_npc.json"
CAARRIGE_RIDER = BASE / "lab04_Carrige_Rider.json"


def run_chat(template_file, name="Agent", **kwargs):
    chat = TemplateChat.from_file(template_file, **kwargs)
    msg = chat.start_chat()

    while True:
        print(f"{name}: {msg}")
        try:
            user = input("You: ")
            msg = chat.send(user)
        except StopIteration:
            break

    return msg


def run_dm():
    dm = TemplateChat.from_file(
        DM_TEMPLATE,
        encounters="npc, carriage_rider"
    )

    msg = dm.start_chat()

    while True:
        print(f"DM: {msg}")

        try:
            user = input("You: ")
            msg = dm.send(user)

            if "ENCOUNTER: npc" in msg:
                print("\n--- NPC encounter begins ---\n")
                run_chat(NPC_TEMPLATE, "NPC")
                break

            if "ENCOUNTER: carriage_rider" in msg:
                print("\n--- Carriage Rider encounter begins ---\n")
                run_chat(CAARRIGE_RIDER, "Carriage Rider")
                break

        except StopIteration:
            break


if __name__ == "__main__":
    run_dm()
