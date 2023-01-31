from rich.console import Console
import os
from time import sleep


c = Console()


class Object:
    def __init__(self, name, interaction, state) -> None:
        self.name: str = name
        self.interaction: str = interaction
        self.state: list = state

    def show(self) -> str:
        text = f"{self.name}\n [yellow]-[/] {self.interaction}"
        return text

    def interact(self, user_input, choices) -> str:
        if user_input == "bk":
            return "bk"

        for (id, state) in enumerate(choices):
            if user_input == state:
                print(self.state[id])
                return self.state[id]

        print("[red]Invalid choice")


# Innitialize test --------------------------------------------------------------------------------
door = Object("Door", "Open the door", ["It is closed", "It is open"])

while True:
    os.system("cls")
    c.print(door.show())
    if door.interact(input("\n(y, n, bk) >>> "), ["n", "y"]) == "bk":
        break
    sleep(1)


print("Out of da loop")
