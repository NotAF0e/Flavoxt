# Some name keys:
# - For objects:
#   - OA: Object access

from rich.console import Console
import os
# from time import sleep

c = Console()


class Object:
    def __init__(self, name: str, interaction: str = None, user_interaction_text: list = None,
                 state: int = None, states: list = None, function: dict = None) -> None:
        self.name: str = name
        self.interaction: str = interaction
        self.user_interaction_text: list = user_interaction_text
        self.states: list = states
        self.state: int = state
        self.function: dict = function

    def show(self) -> str:
        # Temporary: Soon all objects will be handled to stop errors
        if self.interaction == None:
            text = f"{self.name}\n"
        else:
            text = f"{self.name}\n [yellow]-[/] {self.states[self.state]}\n"

        return text

    def interact(self, user_input: str, choices: list) -> str:
        if user_input == "bk":
            return "bk"

        for (id, state) in enumerate(choices):
            if user_input == state:
                self.state = id
                # print(self.states[id])

                return self.states[id]

        c.print("[red]Invalid choice")


class ObjectContainer:
    global Object

    def __init__(self, name: str, objects: list) -> None:
        self.name: list = name
        self.objects: list = objects

    def show(self) -> str:
        text = "In [bold]" + self.name + "[/]\n\n"

        for obj_or_objc in self.objects:
            try:
                text += str(Object.show(obj_or_objc)) + "\n"
            except AttributeError:
                print("WOULD HAVE BEEN AN ERROR DUE TO CONTAINER")
        return text

    def try_enter(self, object_access_obj) -> bool:
        for (id, obj) in enumerate(self.objects):
            try:
                if (obj.function[id] == "OA"
                    ) and (
                        object_access_obj in self.objects):
                    return True
                else:
                    return False
            except AttributeError:
                # Otherwise crash due to object container
                pass

    def interact(self):
        for (id, obj) in enumerate(self.objects):
            try:
                player_input = c.input(
                    obj.user_interaction_text[0]).strip().lower()
                if player_input == "bk":
                    return player_input
                Object.interact(obj, player_input,
                                obj.user_interaction_text[1])
            except (AttributeError, TypeError):
                # Otherwise crash due to object container
                pass


def player_move_location(move_to):
    global player_location
    global global_container

    if move_to is None:
        return player_location

    # This for loop checks existance of all object containers in the global_container
    for container in global_container.objects:
        # print(move_to, container.name)
        try:
            for obj in container.objects:
                # print(object.name)
                if move_to.name == obj.name:
                    player_location = move_to
                    return player_location
        except TypeError:
            # Otherwise crash due to object container
            pass

        if move_to.name == container.name:
            player_location = move_to
            return player_location


def location():
    global global_container
    global player_location

    for container in global_container.objects:
        if container in global_container.objects and player_location == container:
            return container


def player_move_between_containers(container1, container2, object_access_obj):
    global player_location

    if object_access_obj in (container1.objects and container2.objects) and "OA" in object_access_obj.function:
        if player_location != container1:
            if c.input(f"Enter [bold]{container1.name}[/] [green]'y'[/], [red]'n'[/]: ").strip().lower() == "y":
                return container1
        else:
            if c.input(f"Enter [bold]{container2.name}[/] [green]'y'[/], [red]'n'[/]: ").strip().lower() == "y":
                return container2


# Innitialize test --------------------------------------------------------------------------------
airlock = Object(name="airlock", interaction="Open the airlock",
                 user_interaction_text=["Open it [green]'y'[/], Close it [red]'n'[/], bk: ", ["n", "y"]], state=0,
                 states=["It is closed", "It is open"], function=["OA"])
box = Object(name="box")

room2 = ObjectContainer(name="room2", objects=[airlock, box])
room1 = ObjectContainer(name="room1", objects=[airlock])

global_container = ObjectContainer(
    name="Global Container", objects=[room1, room2])

player_location = room1

while True:
    os.system("cls")

    c.print(location().show())

    if player_location == room1:
        if room1.interact() == "bk":
            break
    elif player_location == room2:
        if room2.interact() == "bk":
            break

    if airlock.state == 1:
        os.system("cls")

        c.print(location().show())
        player_location = player_move_location(
            player_move_between_containers(room1, room2, airlock))

    # sleep(0.5)


print("Out of da loop")
