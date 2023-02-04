# Some name keys:
# - For objects:
#   - OA: Object access

from rich.console import Console
import os
from time import sleep

c = Console()


class Object:
    def __init__(self, name: str, interaction: str, state: int, states: list, function: dict) -> None:
        self.name: str = name
        self.interaction: str = interaction
        self.states: list = states
        self.state: int = state
        self.function: dict = function

    def show(self) -> str:
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

        print("[red]Invalid choice")


class ObjectContainer:
    global Object

    def __init__(self, name: str, objects: list) -> None:
        self.name: list = name
        self.objects: list = objects

    def show(self) -> str:
        text = self.name + "\n\n"

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


def player_move_location(move_to):
    global location
    global global_container

    # This for loop checks existance of all object containers in the global_container
    for container in global_container.objects:
        # print(move_to, container.name)
        try:
            for object in container.objects:
                # print(object.name)
                if move_to == object.name:
                    location.clear()
                    location.append(move_to)
                    return location
        except TypeError:
            pass

        if move_to == container.name:
            location.clear()
            location.append(move_to)
            return location


# Innitialize test --------------------------------------------------------------------------------
airlock = Object(name="airlock", interaction="Open the airlock", state=0,
                 states=["It is closed", "It is open"], function=["OA"])

room2 = ObjectContainer(name="room2", objects=[airlock])
room1 = ObjectContainer(name="room1", objects=[airlock, room2])

global_container = ObjectContainer(
    name="Global Container", objects=[room1, room2])

location = ['room1']

while True:
    os.system("cls")
    c.print(room1.show())
    if room2.try_enter(object_access_obj=airlock) and airlock.state == 1:
        c.print("In:" + str(player_move_location("room2")))
    if airlock.interact(input("(y, n, bk) >>> "), ["n", "y"]) == "bk":
        break
    sleep(0.5)


print("Out of da loop")
