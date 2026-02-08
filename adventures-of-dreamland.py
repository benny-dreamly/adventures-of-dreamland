import tkinter
import json
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from PIL import ImageTk, Image
from pathlib import Path
import services
from GameObject import GameObject
from location_ids import Location
from locations_data import LOCATIONS
from objects_data import OBJECT_DEFS
from objects_builder import build_objects, normalize

SAVE_DIR = Path("saves")
SAVE_DIR.mkdir(exist_ok=True)

def normalize_input(text):
    """Normalize input to lowercase and remove spaces/underscores for matching."""
    return text.strip().lower().replace(" ", "").replace("_", "")


class GameState:
    def __init__(self):
        # Location and game flow
        self.current_location = Location.CELL_1
        self.end_of_game = False
        self.playing = False

        # Object state flags
        self.object_flags = {
            "door_open": False,
            "safe_open": False,
            "trapdoor_open": False,
            "fire_lit": False,
            "benny_dead": False,
            "broom_destroyed": False,
            "fire_extinguished": False,
            "three_pieces_solved": False
        }

        # Refresh flags
        self.refresh_location = True
        self.refresh_objects_visible = True

        # Inventory
        self.inventory = []

        # Game objects
        self.objects, self.name_to_id = build_objects(OBJECT_DEFS)
        self.game_objects = list(self.objects.values())

    # Helper methods
    def get_object(self, obj_id):
        obj = self.objects.get(obj_id.lower())  # normalize
        if not obj:
            print(f"[WARNING] Object '{obj_id}' not found!")
        return obj

    def get_object_by_name(self, name):
        """Get object by player-typed name (normalized)."""
        norm_name = normalize_input(name)
        obj_id = self.name_to_id.get(norm_name)
        if not obj_id:
            print(f"[WARNING] Object '{name}' not found!")
            return None
        return self.objects[obj_id]

    def is_carried(self, obj):
        return getattr(obj, "carried", False)

    def set_flag(self, flag_name, value=True):
        if flag_name in self.object_flags:
            self.object_flags[flag_name] = value

    def get_flag(self, flag_name):
        return self.object_flags.get(flag_name, False)

    def add_to_inventory(self, obj):
        if obj not in self.inventory:
            self.inventory.append(obj)
            obj.carried = True
            obj.visible = False

    def remove_from_inventory(self, obj):
        if obj in self.inventory:
            self.inventory.remove(obj)
            obj.carried = False
            obj.visible = True

    def has_in_inventory(self, obj_id):
        return any(item.id.lower() == obj_id.lower() for item in self.inventory)

    # --- Object & Puzzle Logic ---

    def is_visible(self, obj, current_location):
        """Return True if object should be visible in the current room."""

        # Always visible if carried
        if obj.carried:
            return True

        # Locked by progression? never visible by location alone
        if getattr(obj, "progression_locked", False):
            return False

        # Check if inside a container
        loc = obj.location
        if isinstance(loc, GameObject):
            # If the container is not carried or visible, obj is invisible
            if not loc.carried and not loc.visible:
                return False
            # Recursively check container visibility
            return self.is_visible(loc, current_location)

        # loc is a Location enum
        return loc == current_location

    def update_visibility(self):
        for obj in self.objects.values():
            if obj.carried:
                obj.visible = True
            elif obj.visibility_condition:
                obj.visible = obj.visibility_condition(self)
            else:
                obj.visible = self.is_visible(obj, self.current_location)

    def handle_special_conditions(self):
        """Check for game-over conditions or winning."""
        cause_of_death = ""

        # Fire kills Benny if bucket not used
        if self.get_flag("fire_lit") and self.current_location == 22 and not self.has_in_inventory("BUCKET_FILLED"):
            cause_of_death = "a fire."
            self.set_flag("benny_dead", True)

        # Deaths
        if self.get_flag("benny_dead"):
            print_to_description("Benny has died due to " + cause_of_death)
            print_to_description("GAME OVER")
            self.end_of_game = True

        if self.get_flag("broom_destroyed") and not self.get_flag("three_pieces_solved"):
            print_to_description("Benny can't continue to escape, as he used the broom to make a fire before using it for something else.")
            print_to_description("GAME OVER")
            self.end_of_game = True

        # Win condition
        if self.current_location == 23:
            print_to_description("You successfully helped Benny escape the castle basement! Congratulations.")
            self.end_of_game = True

    def describe_visible_objects(self):
        """Update the description widget with objects visible in the current location."""
        if not description_widget:
            return

        visible_objs = [
            obj.name for obj in self.game_objects
            if obj.visible and not obj.carried and obj.location == self.current_location
        ]

        if visible_objs:
            print_to_description("Benny sees " + ", ".join(visible_objs) + ".")
        else:
            print_to_description("Benny sees nothing special.")

    def to_dict(self):
        return {
            "current_location": int(self.current_location),
            "end_of_game": self.end_of_game,
            "object_flags": self.object_flags,
            "objects": {
                obj.name: {
                    "carried": obj.carried,
                    "visible": obj.visible,
                    "location": serialize_location(obj.location)
                }
                for obj in self.game_objects
            }
        }

# --- Object Interaction Helpers ---

def get_obj(name, must_be_visible=True, must_be_in_inventory=False):
    """
    Return the object by name if it meets the requirements.

    Args:
        name (str): object name
        must_be_visible (bool): only return if visible in current location
        must_be_in_inventory (bool): only return if carried

    Returns:
        Object or None
    """
    obj = state.get_object(name)
    if not obj:
        return None
    if must_be_visible and not obj.visible:
        return None
    if must_be_in_inventory and not obj.carried:
        return None
    return obj

def is_carried(name):
    """Check if the object is currently in the player's inventory."""
    obj = state.get_object(name)
    return obj.carried if obj else False

def in_inventory(name):
    """Check if an object (by name or object) is in the inventory."""
    return state.has_in_inventory(name)

def can_take(name):
    """Check if the player can pick up an object."""
    obj = get_obj(name, must_be_visible=False)  # <— FIXED
    return obj is not None and getattr(obj, "movable", False) and not obj.carried

def can_use(name):
    """Check if an object can be used in the current location."""
    obj = get_obj(name, must_be_visible=False, must_be_in_inventory=True)  # <— FIXED
    return obj is not None

def serialize_location(loc):
    if loc is None:
        return None

    if isinstance(loc, Location):
        return {
            "type": "location",
            "id": int(loc)
        }

    # GameObject location
    if hasattr(loc, "name"):
        return {
            "type": "object",
            "id": loc.name
        }

    raise TypeError(f"Invalid location type: {type(loc)}")


def deserialize_location(loc_data, state):
    if loc_data is None:
        return None

    if loc_data["type"] == "location":
        return Location(loc_data["id"])

    if loc_data["type"] == "object":
        return state.get_object(loc_data["id"])

    raise ValueError(f"Unknown location reference: {loc_data}")


PORTRAIT_LAYOUT = True

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None
button_frame = None

playing = False
MAX_TIME_ELAPSED = 15

def perform_command(verb, noun):

    if verb in ["GO", "N", "S", "E", "W", "A", "D", "NORTH", "SOUTH", "EAST", "WEST"]:
        perform_go_command(verb)
    elif verb in ["GET", "TAKE", "GRAB"]:
        perform_get_command(noun)
    elif verb in ["PUT", "DROP"]:
        perform_put_command(noun)
    elif verb in ["LOOK", "INVESTIGATE"]:
        perform_look_command(noun)
    elif verb == "READ":
        perform_read_command(noun)
    elif verb == "OPEN":
        perform_open_command(noun)
    elif verb == "HELP":
        perform_help_command(noun)
    elif verb == "SOLVE":
        perform_solve_command(noun)
    elif verb == "UNLOCK":
        perform_unlock_command(noun)
    elif verb == "DECIPHER":
        perform_decipher_command(noun)
    elif verb == "GLUE":
        perform_glue_command(noun)
    elif verb == "USE":
        perform_use_command(noun)
    elif verb == "FILL":
        perform_fill_command(noun)
    elif verb == "SAVE":
        perform_save_command(noun)
    elif verb == "LOAD":
        perform_load_command(noun)
    else:
        print_to_description("unknown command")

def perform_save_command(slot):
    slot = slot.strip()
    filename = f"save_{slot}.json" if slot else "save.json"
    save_game(filename)

def perform_load_command(slot):
    slot = slot.strip()
    filename = f"save_{slot}.json" if slot else "save.json"
    load_game(filename)

def perform_go_command(direction):
    new_location = get_location(direction, state.current_location)
    if new_location == 0:
        print_to_description("You can't go that way!")
    else:
        state.current_location = new_location
        state.refresh_location = True

def perform_get_command(obj_name):
    print(f"received object: {obj_name}")
    input_text = normalize_input(obj_name)
    obj = state.get_object(input_text)
    if not obj or not can_take(input_text):
        print_to_description("You can't pick that up!")
        return

    state.add_to_inventory(obj)
    print_to_description(f"You pick up the {obj.name}.")
    state.refresh_objects_visible = True

def perform_put_command(obj_name):
    obj = state.get_object(obj_name)
    if not obj:
        print_to_description("You are not carrying one of those!")
        return

    state.remove_from_inventory(obj)
    obj.location = state.current_location
    print_to_description(f"You put down the {obj.name}.")
    state.refresh_objects_visible = True

def perform_look_command(obj_name):
    obj = state.get_object(obj_name)
    if obj and (obj.carried or (obj.visible and obj.location == state.current_location)):
        print_to_description(obj.description)
    else:
        print_to_description("You can't see one of those!")

def perform_read_command(object_name):
    game_object = state.get_object(object_name)

    if game_object is None:
        print_to_description(f"I am not sure which {object_name} you are referring to")
        return

    if not getattr(game_object, "carried", False):
        print_to_description("You're not carrying anything readable")
        return

    if hasattr(game_object, "on_read") and callable(game_object.on_read):
        game_object.on_read()
    else:
        print_to_description("There's nothing readable about this.")


def perform_open_command(object_name):
    game_object = state.get_object(object_name)

    if not (game_object is None):
        safe = state.get_object("safe")
        trapdoor = state.get_object("trapdoor")
        broom = state.get_object("broom")

        if game_object == safe and (game_object.visible and game_object.location == state.current_location) and state.get_flag("safe_open"):
            print_to_description("Benny pulls on the handle and the safe opens!")
            set_current_image()
            game_object.description = "a small safe, with the door wide open"
        elif game_object == trapdoor and (game_object.visible and game_object.location == state.current_location) and broom.carried:
            print_to_description("Benny pushes on the trapdoor with the end of the broom and it opens, revealing a puzzle piece.")
            state.set_flag("trapdoor_open", True)
            state.refresh_objects_visible = True
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")

list_of_commands = ["GO", "N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST", "GET", "READ", "OPEN", "HELP"]

def perform_help_command(_):
    print_to_description("Available commands:")
    print_to_description(", ".join(list_of_commands))

PUZZLE_STAGES = [
    {
        "puzzle": "puzzle",
        "piece": "puzzle_piece_1",
        "next_puzzle": "puzzle_with_one_piece_inserted",
        "remove_objects": ["puzzle_piece_1", "hint1", "clue1", "clue11", "clue2", "puzzle"],
        "slot": 1,
        "next_commands": ["DECIPHER", "SOLVE"]
    },
    {
        "puzzle": "puzzle_with_one_piece_inserted",
        "piece": "puzzle_piece_2",
        "next_puzzle": "puzzle_with_two_pieces_inserted",
        "remove_objects": ["puzzle_piece_2", "puzzle_with_one_piece_inserted", "gold_bar", "bar_clue"],
        "slot": 2,
        "next_commands": ["UNLOCK"]
    },
    {
        "puzzle": "puzzle_with_two_pieces_inserted",
        "piece": "puzzle_piece_3",
        "next_puzzle": "puzzle_with_three_pieces_inserted",
        "remove_objects": ["puzzle_with_two_pieces_inserted", "puzzle_piece_3", "hint3", "fragment_clue", "magnifying_glass"],
        "slot": 3,
        "set_flag": ("three_pieces_solved", True)
    },
    {
        "puzzle": "puzzle_with_three_pieces_inserted",
        "piece": "puzzle_piece_4",
        "next_puzzle": None,
        "remove_objects": ["puzzle_with_three_pieces_inserted", "puzzle_piece_4", "bucket_filled", "lighter"],
        "slot": 4,
        "final_action": lambda: (
            print_to_description("Benny watches as the puzzle transforms into a key. He can finally escape!!!"),
            state.add_to_inventory(state.get_object("key"))
        )
    }
]


def perform_solve_command(object_name):
    """Handles inserting puzzle pieces into the puzzle dynamically."""
    game_object = state.get_object(object_name)
    if not game_object:
        print_to_description("You can't do that.")
        return

    # Find the stage that matches the current puzzle object
    stage = next((s for s in PUZZLE_STAGES if state.get_object(s["puzzle"]) == game_object), None)
    if not stage:
        print_to_description("You're missing something.")
        return

    piece_obj = state.get_object(stage["piece"])
    if not piece_obj or not piece_obj.carried:
        print_to_description("It looks like you don't have anything to put into the puzzle.")
        return

    answer = simpledialog.askstring("Input", f"What would you like to put in the puzzle?", parent=root)
    if answer != stage["piece"].replace("_", " "):
        print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
        return

    # Ask for the slot number until correct
    inserted = False
    while not inserted:
        slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?", parent=root)
        if slot != stage["slot"]:
            print_to_description("The piece won't fit, no matter how you rotate it.")
            retry = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
            if retry.lower() == "no":
                return
        else:
            print_to_description("The piece slots into the puzzle, but you still haven't solved it.")
            inserted = True

    # Remove all relevant objects from inventory/visibility
    for obj_name in stage.get("remove_objects", []):
        obj = state.get_object(obj_name)
        if obj:
            obj.carried = False
            obj.visible = False

    # Set next puzzle state or handle final action
    next_puzzle_name = stage.get("next_puzzle")
    if next_puzzle_name:
        next_puzzle = state.get_object(next_puzzle_name)
        if next_puzzle:
            next_puzzle.carried = True

    # Set any flags
    if "set_flag" in stage:
        flag_name, value = stage["set_flag"]
        setattr(state, flag_name, value)

    # Execute final action if defined
    if "final_action" in stage:
        stage["final_action"]()

    # Add next commands if any
    for cmd in stage.get("next_commands", []):
        state.list_of_commands.append(cmd + "\n")

    state.refresh_objects_visible = True

def perform_glue_command(object_name):
    """Glue fragments together if the player has the glue stick and all pieces."""
    game_object = state.get_object(object_name)

    if game_object is None:
        print_to_description("You can't do that.")
        return

    glue_stick = state.get_object("glue_stick")
    if not glue_stick or not glue_stick.carried:
        print_to_description("You're missing something.")
        return

    # Gather all hint fragments dynamically
    fragments = [state.get_object(f"hint_fragment_{i}") for i in range(1, 14)]

    if all(f and f.carried for f in fragments) and getattr(game_object, "glueable", False):
        print_to_description(
            "Benny succeeds at gluing the fragments of this hint together. "
            "Maybe it will be a bit easier to decipher now?"
        )
        # Remove fragments and original object from inventory/visibility
        for item in fragments + [game_object]:
            if item:
                item.carried = False
                item.visible = False

        # Place the completed hint into inventory
        hint3 = state.get_object("hint3")
        if hint3:
            hint3.carried = True
        state.refresh_objects_visible = True
    else:
        print_to_description("You don't have all the pieces or this can't be glued.")

def perform_unlock_command(object_name):
    """Handle unlocking safes or doors using state-driven logic."""
    game_object = state.get_object(object_name)

    if game_object is None:
        print_to_description("There's nothing to unlock.")
        return

    # Unlock the safe
    if game_object.name.upper() == "SAFE" and game_object.visible and game_object.location == state.current_location:
        safe_obj = game_object  # just for clarity
        if not state.get_flag("safe_open"):
            while True:
                code = simpledialog.askinteger("Code", "What is the code to the safe?", parent=root)
                if code is None:
                    break  # user cancelled input
                encrypted_code = hex(code)
                if encrypted_code != "0x3ffa":
                    print_to_description("Benny tries your code, but the safe won't open.")
                    retry = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                    if retry is None or retry.lower() == "no":
                        break
                else:
                    print_to_description("The code you provided Benny with worked! The safe is now unlocked.")
                    state.set_flag("safe_open", True)
                    break
        state.refresh_objects_visible = True

    # Unlock the door
    elif game_object.name.upper() == "DOOR" and game_object.visible and game_object.location == state.current_location:
        key_obj = state.get_object("key")
        if key_obj and state.has_in_inventory(key_obj):
            state.set_flag("door_open", True)
            set_current_image()
            print_to_description("You unlock the door with the key.")
        else:
            print_to_description("You don't have anything to unlock the door with.")

    else:
        print_to_description("You can't unlock that.")

def perform_decipher_command(message):
    message = message.upper()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    deciphered_message = ""

    key = simpledialog.askinteger("Key", "What would you like to use to decipher the message?", parent=root)

    for letter in message:
        if letter in alpha:  # if the letter is actually a letter
            # find the corresponding ciphertext letter in the alphabet
            letter_index = (alpha.find(letter) - key) % len(alpha)

            deciphered_message = deciphered_message + alpha[letter_index]
        else:
            deciphered_message = deciphered_message + letter

    print_to_description("Deciphered message:")
    print_to_description(deciphered_message)

def perform_fill_command(obj_name):
    obj = state.get_object(obj_name)
    if not obj:
        print_to_description("You can't fill that!")
        return

    bucket = state.get_object("bucket")
    bucket_filled = state.get_object("bucket_filled")
    water = state.get_object("water")

    if obj == bucket and state.current_location == 22:
        print_to_description("Benny dips the bucket into the water and fills it.")
        bucket.carried = False
        bucket.visible = False
        water.visible = False
        bucket_filled.carried = True
    else:
        print_to_description("You can't fill that here, there isn't any water to fill it.")

def perform_use_command(obj_name):
    obj = get_obj(obj_name, must_be_in_inventory=True)
    if not obj:
        print_to_description("You can't use that!")
        return

    if obj.name.upper() == "LIGHTER":
        broom = get_obj("broom")
        if state.current_location == 22 and broom and broom.visible:
            print_to_description("Benny lights the broom with the lighter and watches it burn!")
            state.set_flag("fire_lit", True)
            broom.visible = False
            state.remove_from_inventory(obj)
            state.set_flag("broom_destroyed", True)
        else:
            print_to_description("There's nothing to light on fire.")

    elif obj.name.upper() == "BUCKET_FILLED":
        if state.current_location == 22 and state.get_flag("fire_lit"):
            print_to_description("Benny throws the water onto the fire and manages to put it out!")
            state.set_flag("fire_lit", False)
            state.set_flag("fire_extinguished", True)
            state.remove_from_inventory(obj)
            bucket = get_obj("bucket")
            if bucket:
                state.add_to_inventory(bucket)
        else:
            print_to_description("You can't use that here.")

    else:
        print_to_description("You can't use that.")

def describe_current_location(current_location):
    data = LOCATIONS.get(current_location)

    if data:
        print_to_description(data.name)
        print_to_description(data.desc)
    else:
        print_to_description(f"Unknown location: {current_location}")

def set_current_image():
    """Update the image_label based on the current location and relevant object flags."""
    loc = state.current_location

    # Predefined static images
    static_images = {
        1: 'cell_1.tiff',
        2: 'cell_2.tiff',
        3: 'cell_3.tiff',
        4: 'hallway.tiff',
        5: 'hallway.tiff',
        6: 'right_corner.tiff',
        7: 'hallway_one_door.tiff',
        8: 'vault-1.tiff',
        9: 'vault-2.tiff',
        12: 'left_corner.png',
        13: 'hallway.tiff',
        14: 'right_corner.tiff',
        15: 'hallway.tiff',
        16: 'hallway.tiff',
        17: 'hallway.tiff',
        18: 'hallway.tiff',
        19: 'left_corner.png',
        20: 'hallway_two_doors.tiff',
        21: 'room_21.tiff',
        22: 'room_22.tiff',
        23: 'stairs.tiff'
    }

    # Start with a static default if it exists
    image_file = static_images.get(loc, 'missing.png')

    # Dynamic images based on objects or flags
    if loc == 10:  # Safe room
        safe = state.get_object("safe")
        puzzle2 = state.get_object("puzzle_piece_2")
        puzzle_inserted = state.get_object("puzzle_with_two_pieces_inserted")

        if state.get_flag("safe_open") and puzzle2.visible:
            image_file = 'safe-open.tiff'
        elif puzzle2.carried and not puzzle_inserted.carried:
            image_file = 'open-safe-no-piece.tiff'
        else:
            image_file = 'safe-closed.tiff'

    elif loc == 11:  # Vault room
        gold_bar = state.get_object("gold_bar")
        scroll_hint = state.get_object("scroll_hint")

        if gold_bar.visible and scroll_hint.visible:
            image_file = 'vault-4.tiff'
        elif gold_bar.visible:
            image_file = 'vault-4-no-hint.tiff'
        elif scroll_hint.visible:
            image_file = 'vault-4-no-bar.tiff'
        else:
            image_file = 'vault-4-no-bar-no-hint.tiff'

    # Apply the image to the label
    image_label.img = ImageTk.PhotoImage(file=f'res/images/{image_file}')
    image_label.config(image=image_label.img)

def show_popup_image(image_file):
    popup = tkinter.Toplevel(root)

    img = PhotoImage(file=f"res/images/{image_file}")

    label = tkinter.Label(popup, image=img)
    label.image = img  # Keep a reference to the image to prevent garbage collection
    label.pack()

# Unified direction mappings
DIRECTION_MAPS = {
    "NORTH": {3:2, 2:1, 6:7, 7:12, 9:10, 15:14, 16:15, 17:16, 18:17, 19:18},
    "SOUTH": {1:2, 2:3, 7:6, 10:9, 12:7, 14:15, 15:16, 16:17, 17:18, 18:19, 23:20},
    "EAST":  {3:4, 4:5, 5:6, 8:7, 9:8, 10:11, 12:13, 13:14, 20:19, 21:20, 22:21},
    "WEST":  {4:3, 5:4, 6:5, 7:8, 8:9, 11:10, 13:12, 14:13, 19:20, 20:21, 21:22}
}

def get_location(direction, current_location):
    """Return the next location in the given direction or 0 if impossible."""
    direction = direction.upper()
    mapping = DIRECTION_MAPS.get(direction, {})

    # Handle special cases
    if direction == "NORTH" and current_location == 20 and state.get_flag("door_open"):
        return 23

    return mapping.get(current_location, 0)

def describe_current_inventory():
    """Show the player's current inventory in the inventory_widget."""
    if not inventory_widget:
        return  # in case the UI isn't built yet

    if not state.inventory:
        inventory_text = "You are carrying: nothing"
    else:
        inventory_text = "You are carrying: " + ", ".join(obj.name for obj in state.inventory)

    inventory_widget.config(state="normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory_text)
    inventory_widget.config(state="disabled")

def describe_current_visible_objects():
    object_count = 0
    object_list = ""

    for current_object in state.game_objects:
        if (current_object.location == state.current_location) and current_object.visible and not current_object.carried:
            object_list = object_list + (" and " if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    print_to_description("Benny sees " + (object_list + "." if object_count > 0 else "nothing special."))

def build_interface():
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button
    global root
    global button_frame

    root = Tk()
    root.resizable(True, True)
    root.bind('<Configure>', on_window_resize)  # Call on_window_resize on window resize

    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)
    if PORTRAIT_LAYOUT:
        image_label.grid(row=0, column=0, columnspan=3, padx=2, pady=2)
    else:
        image_label.grid(row=0, column=0, rowspan=3, columnspan=1, padx=2, pady=2)

    description_widget = Text(root, width=60, height=10, relief=GROOVE, wrap='word')
    description_widget.insert(1.0, """After the catastrophe that was the pandemic, Benny finds himself back in dreamland, but something seems wrong. It looks like Fala and Nodo have taken him prisoner! Now he has to use all of the knowledge he’s gathered throughout all of his various adventures in the past to escape.
    
Fala and Nodo have hidden various puzzles throughout the castle basement. Can you figure them out and help Benny escape before evil takes over the kingdom? You’re the kingdom’s only hope at rescuing the protector of Dreamland.
    """)
    description_widget.insert(END, "\n")
    description_widget.config(state="disabled")
    if PORTRAIT_LAYOUT:
        description_widget.grid(row=1, column=0, columnspan=3, sticky=W, padx=2, pady=2)
    else:
        description_widget.grid(row=0, column=1, rowspan=1, columnspan=2, padx=2, pady=2)

    command_widget = ttk.Entry(root, width=(25 if PORTRAIT_LAYOUT else 54), style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    if PORTRAIT_LAYOUT:
        command_widget.grid(row=2, column=0, padx=2, pady=2)
    else:
        command_widget.grid(row=1, column=1, rowspan=1, columnspan=2)

    button_frame = ttk.Frame(root)
    button_frame.config(height=150, width=150, relief=GROOVE)
    if PORTRAIT_LAYOUT:
        button_frame.grid(row=3, column=0, columnspan=1, padx=2, pady=2)
    else:
        button_frame.grid(row=2, column=1, columnspan=1, padx=2, pady=2)

    north_button = ttk.Button(button_frame, text="N", width=5)
    north_button.grid(row=0, column=1, padx=2, pady=2)
    north_button.config(command=north_button_click)

    south_button = ttk.Button(button_frame, text="S", width=5)
    south_button.grid(row=2, column=1, padx=2, pady=2)
    south_button.config(command=south_button_click)

    east_button = ttk.Button(button_frame, text="E", width=5)
    east_button.grid(row=1, column=2, padx=2, pady=2)
    east_button.config(command=east_button_click)

    west_button = ttk.Button(button_frame, text="W", width=5)
    west_button.grid(row=1, column=0, padx=2, pady=2)
    west_button.config(command=west_button_click)

    inventory_widget = Text(root, width=(30 if PORTRAIT_LAYOUT else 38), height=(8 if PORTRAIT_LAYOUT else 6),
                            relief=GROOVE, state=DISABLED)
    if PORTRAIT_LAYOUT:
        inventory_widget.grid(row=2, column=2, rowspan=2, padx=2, pady=2, sticky=W)
    else:
        inventory_widget.grid(row=2, column=2, rowspan=2, padx=2, pady=2, sticky=W)

def on_window_resize(event):
    global button_frame

    # Update the elements upon window resize
    if PORTRAIT_LAYOUT:
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        description_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
        command_widget.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Adjust the button frame to span all columns, align left
        button_frame.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky="w")
    else:
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        description_widget.grid(row=0, column=1, rowspan=1, columnspan=2, sticky="nsew")
        command_widget.grid(row=1, column=1, rowspan=1, columnspan=2, sticky="ew")

        # Place the button frame below the text and input elements, center horizontally
        button_frame.grid(row=2, column=1, columnspan=1, padx=2, pady=10, sticky="nsew")

def set_current_state():
    """Update all UI elements to match the current game state."""
    if state.refresh_location:
        describe_current_location(state.current_location)
        set_current_image()

    if state.refresh_location or state.refresh_objects_visible:
        state.update_visibility()
        set_current_image()
        state.describe_visible_objects()

    state.handle_special_conditions()
    set_directions_to_move()

    if not state.end_of_game:
        describe_current_inventory()

    # Reset refresh flags
    state.refresh_location = False
    state.refresh_objects_visible = False

    # Enable or disable command input based on game state
    command_widget.config(state=("disabled" if state.end_of_game else "normal"))

def north_button_click():
    print_to_description("N", True)
    perform_command("NORTH", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("SOUTH", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("EAST", "")
    set_current_state()

def west_button_click():
    print_to_description("WEST", True)
    perform_command("WEST", "")
    set_current_state()

def return_key_enter(event):
    if event.widget == command_widget:
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun)

        set_current_state()

def set_directions_to_move():
    """Enable or disable movement buttons based on available directions and game state."""
    directions = {
        "NORTH": north_button,
        "SOUTH": south_button,
        "EAST": east_button,
        "WEST": west_button
    }

    for direction, button in directions.items():
        # Check if there is a valid location in that direction and the game isn't over
        can_move = get_location(direction, state.current_location) > 0 and not state.end_of_game
        button.config(state="normal" if can_move else "disabled")

def print_to_description(output, user_input=False):
    description_widget.config(state='normal')
    description_widget.insert(END, output + "\n")
    if user_input:
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground='blue')
    description_widget.insert(END, '\n')
    description_widget.config(state='disabled')
    description_widget.see(END)

def play_audio(filename, asynchronous=True, loop=True):
    import platform
    operating_system = platform.system()

    if operating_system == 'Linux':
        from replit import audio
        sound = audio.play_file(filename)
        sound = audio.play_file('res/cold-moon.wav')
        sound.paused = False
        # according to documentation, setting .set_loop to -1 should create infinite loop in replit. Can't get it to work
        sound.set_loop(-1)
    elif operating_system == 'Windows':
        import winsound
        winsound.PlaySound(filename, winsound.SND_FILENAME +
                           (winsound.SND_ASYNC if asynchronous else 0) +
                           (winsound.SND_LOOP if loop else 0)
                           )
    elif operating_system == 'darwin':
        import os
        while playing:
            os.system('afplay res/audio/{}'.format(filename))
    else:
        print_to_description("unsupported platform")

def save_game(filename):
    data = state.to_dict()
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print_to_description(f"Game saved to {filename}")

def load_game(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print_to_description("No save file found.")
        return

    # --- Core state ---
    state.current_location = Location(data["current_location"])
    state.end_of_game = data["end_of_game"]
    state.object_flags = data["object_flags"]

    # --- Pass 1: restore simple object state ---
    for obj_name, obj_data in data["objects"].items():
        obj = state.get_object(obj_name)
        if not obj:
            continue

        obj.carried = obj_data["carried"]
        obj.visible = obj_data["visible"]
        obj.location = None  # temporary

    # --- Pass 2: restore locations (objects + rooms) ---
    for obj_name, obj_data in data["objects"].items():
        obj = state.get_object(obj_name)
        if not obj:
            continue

        obj.location = deserialize_location(obj_data["location"], state)

    state.refresh_location = True
    state.refresh_objects_visible = True
    print_to_description(f"Game loaded from {filename}")



def main():
    build_interface()

    services.register_ui(
        print_to_description,
        show_popup_image
    )
    set_current_state()
    root.mainloop()

state = GameState()
main()
